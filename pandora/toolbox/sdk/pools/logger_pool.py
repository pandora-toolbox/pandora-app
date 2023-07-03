import logging
import sys
from datetime import datetime
from logging import Logger
from typing import Dict, Optional

from pandora.commons import Singleton, String, OS
from pandora.toolbox.sdk.services.environments import AppEnvironment
from ..constants import Constants


class DefaultFormatter(logging.Formatter):
    def format(self, record):
        location = '%s.%s:%s' % (record.name, record.funcName, record.lineno)
        msg = '[%s] %-40s [%-5s]: %s' % (self.formatTime(record), location, record.levelname, record.msg)
        record.msg = msg
        return super(DefaultFormatter, self).format(record)


class LoggerPool(metaclass=Singleton):
    DEFAULT_FORMATTER: logging.Formatter = DefaultFormatter()

    loggers: Dict[str, Logger] = {}

    @classmethod
    def __create(cls, name=__name__, level=logging.INFO, enable_stdout: bool = False) -> Logger:
        formatter: logging.Formatter = LoggerPool.DEFAULT_FORMATTER

        if AppEnvironment.is_dev():
            level = logging.DEBUG
            enable_stdout = True

        if String.not_empty(name):
            logger = logging.getLogger(name)

            logger.setLevel(level)
            logger.propagate = False  # Avoids the Logger repeating itself when created via init class

            if enable_stdout:  # Setup StreamHandler for console output
                stdout_handler = logging.StreamHandler(sys.stdout)
                stdout_handler.setLevel(level)
                stdout_handler.setFormatter(formatter)

                logger.addHandler(stdout_handler)

            # Setup File Handler
            if name == "root":
                file_path: str = f"{Constants.HOME_PATH}/data/logs"
                filename: str = f"{name}-{datetime.now().isoformat()}.log"

                OS.Path.touch(file_path, filename)

                file_handler = logging.FileHandler(f"{file_path}/{filename}")
                file_handler.setLevel(level)

                logger.addHandler(file_handler)
        else:
            raise ValueError("Unable to setup logger: Logger Name is empty.")

        return logger

    @staticmethod
    def get(cls: type = None, name: str = None, level: int = logging.INFO,
            enable_stdout: bool = True) -> Logger:
        """
        Get a Logger based on name with the default Log Level as 'INFO'.
        If the Logger does not exist, create a new one.
        Logs will be redirected to `stdout` in DEBUG level if it is a dev environment.
        """
        logger: Optional[Logger] = None

        if cls is not None:
            if String.is_empty(name):
                if isinstance(cls, type):
                    name = cls.__name__
                elif isinstance(cls, str):
                    name = cls
                else:
                    raise ValueError(f"Logger Class '{cls}' is not valid.")
        elif String.is_empty(name):
            raise ValueError(f"Logger do not have a valid class or name.")

        if String.not_empty(name):
            try:
                logger = LoggerPool.loggers[name]
            except KeyError:
                pass
        else:  # Both Logger Class and Name are empty
            raise ValueError("Logger Name is empty.")


        if logger is None:
            logger = LoggerPool.__create(name=name, level=level,
                                         enable_stdout=enable_stdout)

            LoggerPool.loggers[name] = logger

        return logger

    def __str__(self):
        return str(self.__dict__)

    @classmethod
    def root(cls, level=logging.WARN) -> Logger:
        """Creates a 'root' Logger"""
        return LoggerPool.get(name="root", level=level, enable_stdout=True)
