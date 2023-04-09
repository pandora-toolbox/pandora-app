import logging
from logging import Logger
from typing import Dict, Optional

from ..models import Constants, Manifest
from .object_pool import inject
from ..environments import AppEnvironment
from ...commons import Singleton, String


class LoggerPool(metaclass=Singleton):
    DEFAULT_FORMATTER: logging.Formatter = \
        logging.Formatter("[%(asctime)s][%(levelname)s] %(filename)s %(funcName)s (at line %(lineno)d): %(message)s")

    loggers: Dict[str, Logger] = {}

    @inject
    def __init__(self, manifest: Manifest):
        self.manifest: Manifest = manifest

    @classmethod
    def __create(cls, name=__name__, level=logging.INFO, enable_stdout: bool = False) -> Logger:
        from ...commons.integrations import OS
        import logging
        import sys

        if String.not_empty(name):
            logger = logging.getLogger(name)
            logger.setLevel(level)
            formatter = LoggerPool.DEFAULT_FORMATTER

            # If is dev, setup stdout
            if enable_stdout:
                stdout_handler = logging.StreamHandler(sys.stdout)
                stdout_handler.setLevel(logging.DEBUG)
                stdout_handler.setFormatter(formatter)

                logger.addHandler(stdout_handler)

            # Setup File Handler
            file_path: str = f"{Constants.home}/data/logs"
            filename: str = f"{name}.log"

            if not OS.Path.exists(file_path):
                OS.Path.mkdir(file_path)
                OS.Path.touch(file_path, filename)

            file_handler = logging.FileHandler(f"{file_path}/{filename}")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
        else:
            raise ValueError("Unable to setup logger: Logger Name is empty.")

        return logger

    @classmethod
    def __get(cls, name=__name__, level=logging.INFO, enable_stdout: bool = None) -> Logger:
        """
        Get a Logger based on name with the default Log Level as 'INFO'.
        If the Logger does not exist, create a new one.
        The created Logger will log to file at `${PANDORA_HOME}/data/logs/{name}.log by default and it will log
        to `stdout` if it is a dev environment (or if it is the root logger)
        """
        if String.is_empty(name):
            name = "root"

        logger: Optional[Logger] = None

        try:
            logger = cls.loggers[name]
        except KeyError:
            pass

        if logger is None:
            logger = LoggerPool.__create(name=name, level=level,
                                         enable_stdout=AppEnvironment.is_dev()
                                         if enable_stdout is None else enable_stdout)

        cls.loggers[name] = logger

        return logger

    def get(self, name=__name__, level=logging.INFO) -> Logger:
        """
        Get a Logger based on name with the default Log Level as 'INFO'.
        If the Logger does not exist, create a new one.
        The created Logger will log to file at `${PANDORA_HOME}/data/logs/{name}.log by default and it will log
        to `stdout` if it is a dev environment (or if it is the root logger)
        """
        if String.is_empty(name):
            name = "root"

        logger: Optional[Logger] = None

        try:
            logger = self.loggers[name]
        except KeyError:
            pass

        if logger is None:
            logger = LoggerPool.__create(name=name, level=level, enable_stdout=AppEnvironment.is_dev())

        self.loggers[name] = logger

        return logger

    def __str__(self):
        return str(self.__dict__)

    @classmethod
    def root(cls, level=logging.WARN) -> Logger:
        """Creates a 'root' Logger"""
        logger: Logger = LoggerPool.__get(name="root", level=level, enable_stdout=True)
        cls.loggers["root"] = logger

        return logger
