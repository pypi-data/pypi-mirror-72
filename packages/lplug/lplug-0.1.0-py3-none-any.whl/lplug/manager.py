#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
import gc
import glob
import importlib
import logging
import os
import pkgutil
import site
import sys
import threading
import types
import uuid
from collections import namedtuple
from collections.abc import Iterable

import pkg_resources

__all__ = ("PluginManager",)

_HAS_REFCOUNT = hasattr(sys, "getrefcount")
modlogger = logging.getLogger(__name__)
_default_predicate = lambda *_: True


# TODO: make the manager thread safe
class PluginManager(object):
    """
    Manage plugins and them loading/unloading.

    It fetches modules and directories to find valid plugins, then register and save it.

    It can be configured using the :attr:`~PluginManager.settings` attribute,
    or by passing the settings keys through the constructor.

    :param baselist: A list of classes that is used to check plugin inhiterance.
                     If one of these is the base of the plugin,
                     it will be saved into a dedicated array for all the plugins with the same base.
                     With this check, all the objects that are not classes
                     (instances of :class:`type`), are skipped.
                     Default is an empty list, that removes this check.

                     .. tip::
                        If you want to load all the classes,
                        pass `[object]` to this parameter.

    :type baselist: list[type]

    :param namelist: A list of names that plugins must have.
                     If one of these is the name of the plugin in the module,
                     it will be saved into a dedicated array for all the plugins with the same name.
                     Default is an empty list, that removes this check.

    :type namelist: list[str]

    :param bool use_all: `True` to get module attributes from `__all__`,
                         `False` to get module attribute via :func:`dir`,
                         defaults to `True`.
                         If `__all__` in module does not exists or it is not valid,
                         :func:`dir` is used instead.

    :param bool collect_empty_modules: `True` to save modules that have no valid plugins,
                                       `False` otherwise, defaults to `False`.

    :param bool only_public: `True` to not load plugins that have name that starts with "_",
                             `False` otherwise, defaults to `True`.

    :param extra_predicate: A callable that add an extra check to valid plugins.
                            The callable must accept 3 parameters: module, name, plugin;
                            module and name can be None.
                            The callable should return a valid boolean
                            or an object castable into it.

    :type extra_predicate: Callable[[Module, str, object], bool]

    :param bool suppress_error:
        `True` to suppress exceptions on plugin loading, `False` otherwise, defaults to `False`
        Errors are logged in both cases.

    .. seealso::
        `The Python import system <https://docs.python.org/3/reference/import.html>`_.
    """

    # namedtuples
    plugin_attrs = namedtuple("PluginAttrs", ("module", "base", "name"))
    Settings = namedtuple(
        "PluginSettings",
        (
            # feature settings
            "baselist",
            "namelist",
            # collector settings
            "use_all",
            "collect_empty_modules",
            # "suppress_error",
            # filter settings
            "only_public",
            "extra_predicate",
        ))

    logger = modlogger.getChild("manager")

    __slots__ = (
        # "_lock",
        "settings",
        "loaded_objects",
        "attribute_container",
    )

    def __init__(self, **settings):
        super().__init__()
        _default = {
            "baselist": [],
            "namelist": [],
            "use_all": True,
            "only_public": True,
            # "suppress_error": True,
            "collect_empty_modules": False,
            "extra_predicate": _default_predicate,
        }
        _default.update(**settings)
        self.settings = self.Settings(**_default)

        self.loaded_objects = {}
        self.attribute_container = self.plugin_attrs(*(
            {} for _ in range(len(self.plugin_attrs._fields))))

    def __getitem__(self, key) -> list:
        """
        Get plugins by given key.

        The key can be:

        - A class to get all plugins that inhiterit from key.

        - A :class:`str` to get all plugins that have key as name.
        """
        if isinstance(key, type):
            objects = self.attribute_container.base.get(key)

        elif isinstance(key, str):
            objects = self.attribute_container.name.get(key)

        else:
            raise TypeError("Can't get plugins using a {} as key".format(
                type(key).__name__))

        if objects is None:
            return None

        return [self.loaded_objects[x][0] for x in objects]

    def __setitem__(self, key, plugin):
        # """Load a plugin by given key and instance."""
        return NotImplemented

    def __delitem__(self, key):
        #"""Remove plugins by class or by name."""
        return NotImplemented
        # if isinstance(key, (type, str)):
        #     self.remove_plugins(key)
        # raise TypeError("Can't remove plugins using a {} as key".format(
        #     type(key).__name__))

    def _register_object(self, obj, **attrs) -> int:
        """Create an UUID for the object and save it into loaded objects."""
        uid = uuid.uuid4().int
        while uid in self.loaded_objects:
            uid = uuid.uuid4().int

        self.loaded_objects[uid] = (obj, attrs)
        return uid

    def _insert_id_into(self, uid: int, category: str, key):
        """Insert id into given category in a list defined by key."""
        if not hasattr(self.attribute_container, category):
            raise AttributeError(
                "Category {} can't be used because it is not defined.".format(
                    category))

        self.loaded_objects[uid][1][category] = key
        category = getattr(self.attribute_container, category)
        if key in category:
            category[key].append(uid)
        else:
            category[key] = [uid]

    # def copy(self):
    #     """Create a copy of self, that include settings and loaded plugins."""
    #     inst = copy.copy(self)
    #     return inst

    def _load_plugincls(self, plugincls: type) -> bool:
        """
        Register a new plugin class and save it into the right dictionary by its type.

        :param type plugincls: The class to be registered.
        """
        settings = self.settings
        for base in settings.baselist:
            if issubclass(plugincls, base):
                uid = self._register_object(plugincls)
                self._insert_id_into(uid, "base", base)
                return uid
        return None

    def load_plugin(self,
                    plugin: object,
                    name: str = None,
                    module: types.ModuleType = None,
                    uid: int = None) -> bool:
        """
        Register a new plugin class and save it into the right category.
        This method is responsible to check if the plugin can be loaded or not.

        :param object plugin: The object to be registered.

        :param str name: The plugin name. Usually, it is the name in the module.

        :param types.ModuleType module: the module where plugin came from.

        """
        # params processing
        if name is None and isinstance(plugin, type):
            name = plugin.__name__

        # settings variables
        settings = self.settings
        base_enabled = bool(settings.baselist)
        name_enabled = bool(settings.namelist)

        # create checks
        checks = []
        if base_enabled:
            checks.append("isinstance(plugin, type)")
        if name_enabled:
            checks.append("name in settings.namelist")

        # checks.append("predicate(module, name, attr)")

        # probably there is a safer and smarter way to do this
        valid = eval(" and ".join(checks)) and settings.extra_predicate(  # pylint: disable=W0123
            module, name, plugin)
        del checks

        if valid:
            if base_enabled:
                uid = self._load_plugincls(plugin)
            if uid is None or uid not in self.loaded_objects:
                uid = self._register_object(plugin)

            self._insert_id_into(uid, "name", name)

        return uid

    def fetch_module(self, mod: types.ModuleType, path: str = None) -> bool:
        """Fetch a module for finding plugins."""
        settings = self.settings

        # collect module attributes
        if settings.use_all:
            if isinstance(getattr(mod, "__all__", None), Iterable):
                attrs = mod.__all__
            else:
                self.logger.warning(
                    "Module %s has not __all__, fallback to dir()",
                    mod.__name__)
                attrs = dir(mod)
        else:
            attrs = dir(mod)

        if path is None:
            path = mod.__file__

        if settings.only_public:
            attrs = filter(
                lambda name: not name.startswith("_"),
                attrs,
            )

        mod_members = []
        for attrname in attrs:
            if not hasattr(mod, attrname):
                self.logger.debug("Attribute %s isn't exists", attrname)
                continue

            attr = getattr(mod, attrname, None)
            uid = None

            # type check
            uid = self.load_plugin(attr, attrname, module=mod)
            if uid:
                mod_members.append(uid)
                self.logger.info(
                    "Found plugin on %s typed %s",
                    attr.__name__,
                    type(attr.__name__),
                )
            else:
                self.logger.debug("Skip attribute %s typed %s on module %s",
                                  attr,
                                  type(attr).__name__, path)

        # check if at least one plugin was loaded
        if not (mod_members or settings.collect_empty_modules):
            self.logger.warning("Module %s has no valid plugins.", mod.__name__)
            return False

        self.attribute_container.module[path] = []
        for member in frozenset(mod_members):
            self._insert_id_into(member, "module", path)
        return True

    def _remove_mod_refs(self, mod, modname):
        """Remove any reference to the module."""
        if self.logger.isEnabledFor(
                logging.DEBUG) and _HAS_REFCOUNT and mod is not None:
            refcount = sys.getrefcount(mod)
            self.logger.debug("Remaining references to %s modules: %s", modname,
                              refcount - 3 if refcount > 2 else "/")

        # if module_path in sys.path_importer_cache:
        #     self.logger.debug(
        #         "Found a cached module's path, this will be deleted")
        #     del sys.path_importer_cache[module_path]
        # importlib.invalidate_caches()

        if modname in sys.modules:
            del sys.modules[modname]

    def load_module(self, path: str, is_folder: bool = False) -> None:
        """Load a module by given path, then fetch it."""
        if isinstance(path, str):
            _, module_file = os.path.split(path)
            modname, _ = os.path.splitext(module_file)
            modname = "lplug_" + modname

            module_path = path

            if is_folder:
                module_path = os.path.join(module_path, "__init__.py")

            spec = importlib.util.spec_from_file_location(modname, module_path)

            try:
                mod = spec.loader.load_module()
            except Exception as ex:  # pylint: disable=W0703
                self.logger.error(
                    "Failed to load plugin %s from %s",
                    modname,
                    path,
                    exc_info=ex,
                )
                return

            self.logger.debug(
                "Load %s from %s",
                "package" if is_folder else "module",
                path,
            )

        elif isinstance(path, types.ModuleType):
            # Workaround for search_modules
            mod = path
            path = mod.__file__
            modname = mod.__name__
        else:
            raise TypeError("Expected a str, got {}".format(
                type(path).__name__))

        if path not in self.attribute_container.module and self.fetch_module(
                mod):
            pass

        self._remove_mod_refs(mod, modname)

    # module scanning
    def fetch_folder(self,
                     path: str,
                     skip_controls: bool = False,
                     only_dirs: bool = False):
        """
        Fetch a folder for finding plugin modules.
        By default it controls only
        file that doesn't start with _ and end with.py.

        :param bool skip_controls: If True, do no controls in selected modules.
        :param bool only_dirs: If true this load all folders, but not modules.
                               With this flag, the skip_controls has different meaning,
                               It tells if skips the __init__.py check.

        .. tip::
            If you don't need the advanced parameters of this method,
            please use the :meth:`PluginManager.search_modules` method instead.

        .. note::
            It doesn't look into subdirectories.
        """
        if only_dirs:
            globs = "{}{}*".format(
                glob.escape(path),
                os.path.sep,
            )
        elif skip_controls:
            globs = "{}{}*.*".format(
                glob.escape(path),
                os.path.sep,
            )
        else:
            globs = "{}{}*.py".format(
                glob.escape(path),
                os.path.sep,
            )

        self.logger.debug("Selected glob: %s", globs)
        result = glob.glob(globs)
        self.logger.debug("Found files/directories: %s", result)
        _trash_res = []

        if only_dirs:
            checks = (lambda dirpath: not os.path.isfile(os.path.join(dirpath, "__init__.py")),
                      lambda dirpath: dirpath.endswith("__pycache__"))
            for dirpath in result:
                if not os.path.isdir(dirpath) or (skip_controls or any(
                        check(dirpath) for check in checks)):
                    _trash_res.append(dirpath)

        elif not skip_controls:
            checks = (lambda filename: filename.startswith("__"),)
            for filepath in result:
                file = os.path.basename(filepath)

                if not os.path.isfile(filepath) or (skip_controls or any(
                        check(file) for check in checks)):
                    _trash_res.append(filepath)

        for trash in _trash_res:
            result.remove(trash)

        self.logger.info(
            "Found %s %s in the directory %s.",
            len(result),
            "packages" if only_dirs else "modules",
            path,
        )
        for filepath in result:
            self.load_module(filepath, is_folder=only_dirs)

    def search_modules(self,
                       paths: list = "",
                       entry_point: str = "",
                       begin: str = "",
                       end: str = "",
                       no_pkg: bool = False) -> None:
        """
        Elastic module search engine.

        This method implements some methods for finding and loading modules.
        Here are listed:

            by paths
                Given paths.
                Found modules can be filter by module name begin and
                end. Module type (file or folder) can be filtered too.
                Remember that the found modules are in module format.
                (ex. "package.module").

            by entry_point
                This method requires setuptools.
                Given entry point name, that must be setted in the setup.py file.
                Found modules can be filter by module name start and end.
                Module type (file or folder) can be filtered too.
                Remember that the found modules are in module format.
                (ex. "package.module").

        :param list paths: A list of paths to be scanned.
            If this parameter is "site", it becomes
            a list of :mod:`site` paths.

        :param str entry_point: A setuptools entry_point.
            This parameter will be passed to :func:`pkg_resources.iter_entry_points`,
            for getting all the packages market with the entry_point.

        :param str begin: Required begin of the package name.

        :param str end: Required end of the package name.

        :param bool no_pkg: If True, discard all the packages (folders).

        .. versionadded:: 0.4.0

        .. seealso::
            `The Python import system <https://docs.python.org/3/reference/import.html>`_.

            The :mod:`site` module for site packages.

            :func:`pkgutil.iter_modules` and :func:`pkg_resources.iter_entry_points`
            (from setuptools) functions.

            Setuptools `Dynamic Discovery of Services and Plugins
            <https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins>`_
            section.
        """
        logger = self.logger.getChild("search")

        if paths is not None:
            if paths == "site":
                logger.debug("Use site paths.")
                paths = site.getsitepackages() + [site.getusersitepackages()]

            if isinstance(paths, Iterable):

                for finder, name, ispkg in pkgutil.iter_modules(paths):
                    if not (ispkg and no_pkg) and name.startswith(
                            begin) and name.endswith(end):
                        try:
                            mod = finder.find_module(name).load_module(name)
                        except Exception as ex:  # pylint: disable=W0703
                            self.logger.warning(
                                "Failed to load plugin %s from %s",
                                name,
                                finder.path,
                                exc_info=ex)
                            self._remove_mod_refs(None, name)
                            continue

                        self.logger.debug(
                            "Load %s from %s",
                            "package" if ispkg else "module",
                            finder.path,
                        )
                        self.load_module(mod)

                for path in paths:
                    del sys.path_importer_cache[path]

            else:
                raise TypeError("{} is not a valid list of paths".format(paths))

        elif entry_point is not None:
            for entry in pkg_resources.iter_entry_points(entry_point):
                mod = entry.load()
                # self.loaded_modules.append(mod)
                self.fetch_module(mod)

        elif entry_point is not None and pkg_resources is None:
            raise ImportError(
                "The pkg_resources library is not available.\n"
                "Please install it using 'pip install setuptools'")

        else:
            self.logger.warning("Nothing to search")

    # plugin removes
    def remove_plugin_by_id(self, uid: int) -> bool:
        """The remove_plugin_by_id method."""
        if uid is None and uid not in self.loaded_objects:
            return False

        _, attrs = self.loaded_objects[uid]
        del self.loaded_objects[uid]

        for category, value in attrs.items():
            uid_list = getattr(self.attribute_container, category)[value]
            uid_list.remove(uid)
            if not uid_list:
                del getattr(self.attribute_container, category)[value]
        # plugin.deactivate()
        return True

    def remove_plugin(self, plugin: object, use_identity: bool = False) -> bool:
        """The remove_plugin method."""
        uid_to_remove = None
        if use_identity:
            predicate = lambda pair: pair[0] is plugin
        else:
            predicate = lambda pair: pair[0] == plugin

        for (uid, pluginpair) in self.loaded_objects.items():
            if predicate(pluginpair):
                uid_to_remove = uid
                break

        return self.remove_plugin_by_id(uid_to_remove)

    def remove_plugins(self, plugins: list, use_identity: bool = False):
        """The remove_plugins method."""

        uids_to_remove = []
        if use_identity:
            predicate = lambda pair, plugin: pair[0] is plugin
        else:
            predicate = lambda pair, plugin: pair[0] == plugin

        for (uid, pluginpair) in self.loaded_objects.items():
            plugin_to_remove = None
            for i, plugin in enumerate(plugins):
                if predicate(pluginpair, plugin):
                    plugin_to_remove = i
                    break

            if plugin_to_remove is not None:
                del plugins[plugin_to_remove]
                uids_to_remove.append(uid)

        if not uids_to_remove:
            return False

        for uid in uids_to_remove:
            self.remove_plugin_by_id(uid)
        return True

    # module remove
    def remove_module(self, path: str) -> bool:
        """The remove_module method."""
        if path in self.attribute_container.module:
            for uid in iter(self.loaded_objects[x]
                            for x in self.attribute_container.module[path]):
                self.remove_plugin_by_id(uid)

            del self.attribute_container.module[path]

            gc.collect()
            return True

        return False

    def reload_modules(self):
        """Remove and reload all modules."""

        modules = self.attribute_container.module.copy()
        for path in modules:
            self.remove_module(path)

        for mod in modules:
            self.load_module(mod)

        gc.collect()
