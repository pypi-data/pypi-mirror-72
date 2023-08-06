import logging
import logging.config
import yaml
import sys
import re
import os.path
import traceback

from gutools.tools import expandpath, merge_config

exclude = re.compile(r"(self|_.*)", re.DOTALL)
include = re.compile(r"(.*)", re.DOTALL)
#exclude = re.compile(r"(_.*)", re.DOTALL)


def logger(name, path=None, config='logging.yaml'):
    """Get a logger from logger system.
    The config file and handlers are loaded just once
    avoiding to truncate log files when loggers are
    required and returned.

    default folders to find logging yaml configuration file are:

    ~/
    ~/.config/
    <module_path>/
    /etc/

    and all the levels from current path until '/' is reached

    Aplication merges configuration in reverse order like class hierarchy

    """
    log = logging.getLogger(name)
    if not log.handlers:  # it seems like logging is not configured already
        # print(f"Looking for logger: '{name}' ({path}) {'-'*40}")
        conf = merge_config(config, path)

        logging.config.dictConfig(conf)
        log = logging.getLogger(name)
        if not log.handlers:
            print(f"** Logger: '{name}' is not defined in {config}")
            foo = 1
    return log


def trace(message='', context=None, name=None, log=None, exclude=exclude, include=include, level=logging.INFO, frames=1):
    parent = sys._getframe(frames)
    name = name or parent.f_code.co_name

    if context == None:
        context = parent.f_locals

    self = context.get('self')

    if not isinstance(exclude, re.Pattern):
        exclude = re.compile(exclude, re.DOTALL)
    if not isinstance(include, re.Pattern):
        include = re.compile(include, re.DOTALL)

    ctx = dict([(k, v) for k, v in context.items() if include.match(k) and not exclude.match(k)]) \
        or ''

    if not log:
        mod = parent.f_globals
        log = mod.get('log') or logger(mod['__name__'])

    if self:
        label = str(self)
        log.log(level, f"{label:>12}.{name}(): {message} {ctx}")
    else:
        log.log(level, f"{name}(): {message} {ctx}")


def _debug(*args, **kw):
    return trace(level=logging.DEBUG, frames=2, *args, **kw)


def _error(*args, **kw):
    return trace(level=logging.ERROR, frames=2, *args, **kw)


def _warn(*args, **kw):
    return trace(level=logging.WARN, frames=2, *args, **kw)


def _info(*args, **kw):
    return trace(level=logging.INFO, frames=2, *args, **kw)


def debug(*args, **kw):
    kw['context'] = {}
    return trace(level=logging.DEBUG, frames=2, *args, **kw)


def info(*args, **kw):
    kw['context'] = {}
    return trace(level=logging.INFO, frames=2, *args, **kw)


def warn(*args, **kw):
    kw['context'] = {}
    return trace(level=logging.WARN, frames=2, *args, **kw)


def error(*args, **kw):
    kw['context'] = {}
    return trace(level=logging.ERROR, frames=2, *args, **kw)


def exception(*args, **kw):
    #trace(level=logging.ERROR, frames=2, *args, **kw)
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.format_exception(exc_type, exc_value, exc_tb)
    tb = ''.join(tb)
    trace(message=tb, level=logging.ERROR, frames=2)


