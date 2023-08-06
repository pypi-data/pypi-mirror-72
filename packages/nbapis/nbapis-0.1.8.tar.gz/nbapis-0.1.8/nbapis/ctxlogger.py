import logging
from .defs import KEY_CID, KEY_ID

_loggers = {
    'debug': logging.debug,
    'info': logging.info,
    'warn': logging.warn,
    'error': logging.error,
}


def debug(ctx, content):
    _log(ctx, 'debug', content)


def info(ctx, content):
    _log(ctx, 'info', content)


def warn(ctx, content):
    _log(ctx, 'warn', content)


def error(ctx, content):
    _log(ctx, 'error', content)


def _log(ctx, level, content):
    cid = getattr(ctx, KEY_CID, 'unknown')
    uid = getattr(ctx, KEY_ID, 'unknown')
    _loggers.get(level, logging.info)(f'[{cid}|{uid}]: {content}')
