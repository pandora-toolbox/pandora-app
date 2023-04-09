from logging import Logger
from typing import List

from .cli.parser import CLI
from .environments.appenv import AppEnvironment
from .models import Constants, Manifest
from .plugins.management import PluginContainer
from .pools import ObjectPool, resource
from .pools.logger_pool import LoggerPool
from ..commons.serialization import Serializable


class PandoraApp(Serializable):
    logger: Logger = LoggerPool.root()

    manifest: Manifest = Manifest
    objects: ObjectPool = ObjectPool
    loggers: LoggerPool = LoggerPool
    plugins: PluginContainer = PluginContainer

    def __init__(self):
        super().__init__(**AppRuntimeConfig().config())

    def run(self, args: List[str]) -> object:
        command, nargs = CLI(self.plugins.cmd_tree).parse(args)

        return self.plugins.exec(command, args)


class AppRuntimeConfig:
    """
    Configure the application in a Runtime Level, resolving object dependencies, loading environment variables, etc.
    """
    def config(self):
        return {
            "objects": ObjectPool(),
            "manifest": self.manifest(),
            "loggers": LoggerPool(),
            "plugins": self.plugins()
        }

    @resource
    def manifest(self):
        home = Constants.home
        manifest: Manifest = Manifest.load(home)

        if manifest.api_version != "1":
            raise ValueError(f"Pandora API Version (api_version) '{manifest.api_version}' is not valid. " +
                             f"(App Home: '{home}').")

        ObjectPool().add(key=str(AppEnvironment.oid), obj=manifest.preferences.environment)

        return manifest

    @resource
    def plugins(self):
        from src.main.sdk.plugins.management import PluginContainer

        return PluginContainer()
