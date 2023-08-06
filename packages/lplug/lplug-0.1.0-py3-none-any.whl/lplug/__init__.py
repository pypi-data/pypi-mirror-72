#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Root of the lplug source code."""

import logging
import logging.config

from .manager import *
from .manager import __all__ as manager_all

# from .baseplugin import *
# from .baseplugin import __all__ as baseplugin_all
baseplugin_all = ()

__version__ = "0.1.0"
__all__ = ("__version__",) + baseplugin_all + manager_all

# logging global setup


class LevelFilter(logging.Filter):
    """Filter to allow only a level."""

    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Check if record match the level."""
        return record.levelno == self.level or record.levelname == self.level


logging.config.dictConfig(
    dict(
        version=1,
        filters={
            "debug": {
                "()": LevelFilter,
                "level": logging.DEBUG,
            },
            "info": {
                "()": LevelFilter,
                "level": logging.INFO,
            },
            "warning": {
                "()": LevelFilter,
                "level": logging.WARNING,
            },
            "error": {
                "()": LevelFilter,
                "level": logging.ERROR,
            },
            "critical": {
                "()": LevelFilter,
                "level": logging.CRITICAL,
            },
        },
        formatters={
            "debug": {
                "format":
                "[\033[36;1;1m%(levelname)s\033[0m]:%(name)s: %(message)s"
            },
            "info": {
                "format":
                "[\033[32;1;1m%(levelname)s\033[0m]:%(name)s: %(message)s"
            },
            "warning": {
                "format":
                "[\033[33;1;1m%(levelname)s\033[0m]:%(name)s: %(message)s"
            },
            "error": {
                "format":
                "[\033[35;1;1m%(levelname)s\033[0m]:%(name)s: %(message)s"
            },
            "critical": {
                "format":
                "[\033[31;1;1m%(levelname)s\033[0m]:%(name)s: %(message)s"
            },
        },
        handlers={
            "debug": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "debug",
                "filters": ["debug"],
                "stream": "ext://sys.stdout",
            },
            "info": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "info",
                "filters": ["info"],
                "stream": "ext://sys.stdout",
            },
            "warning": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "warning",
                "filters": ["warning"],
                "stream": "ext://sys.stdout",
            },
            "error": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "error",
                "filters": ["error"],
                "stream": "ext://sys.stderr",
            },
            "critical": {
                "class": "logging.StreamHandler",
                "level": "CRITICAL",
                "formatter": "critical",
                "filters": ["critical"],
                "stream": "ext://sys.stderr",
            },
            "outfile": {
                "class": "logging.FileHandler",
                "filename": "lplug.log",
                "encoding": 'utf-8',
                "mode": 'w',
            },
        },
        loggers={
            "lplug": {
                "handlers":
                ["debug", "info", "warning", "error", "critical", "outfile"],
                "level":
                "WARNING",
            },
        },
    ))

try:
    import colorama
except ImportError:
    logging.getLogger("lplug").warning(
        "The colorama library is missing. "
        "On non-ANSI terminals this leads to unwanted characters.")
