import logging
import uuid
import typing

_loggers = {
    'debug': logging.debug,
    'info': logging.info,
    'warn': logging.warn,
    'error': logging.error,
}


class Ctx:
    def __init__(self, auth: str = '', state: typing.Dict = {}):
        super().__setattr__("_state", state)
        self.uid = str(uuid.uuid4())
        self.cid = 'unknown'
        self.auth = auth

    def __setattr__(self, key: typing.Any, value: typing.Any) -> None:
        self._state[key] = value

    def __getattr__(self, key: typing.Any) -> typing.Any:
        try:
            return self._state[key]
        except KeyError:
            message = f"'{self.__class__.__name__}' object has no attribute '{key}'"
            raise AttributeError(message)

    def __delattr__(self, key: typing.Any) -> None:
        del self._state[key]

    def debug(self, content):
        self._log('debug', content)

    def info(self, content):
        self._log('info', content)

    def warn(self, content):
        self._log('warn', content)

    def error(self, content):
        self._log('error', content)

    def _log(self, level, content):
        _loggers.get(level, logging.info)(f'[{self.cid}|{self.uid}]: {content}')
