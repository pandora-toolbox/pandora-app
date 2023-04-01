from logging import Logger

from .components.constants import Constant
from .components.logger_pool import LoggerPool
from .components.manifest import Manifest
from .components.object_pool import ObjectPool, resource
from .environments.appenv import AppEnvironment
from ..commons.integrations import OS
from ..commons.serialization import Serializable


class PandoraApp(Serializable):
    logger: Logger = LoggerPool.root()

    manifest: Manifest = Manifest
    objects: ObjectPool = ObjectPool
    loggers: LoggerPool = LoggerPool

    def __init__(self):
        super().__init__(**AppRuntimeConfig().config())
        self.logger.warning(self.manifest)


class AppRuntimeConfig:
    """
    Configure the application in a Runtime Level, resolving object dependencies, loading environment variables, etc.
    """
    def __init__(self):
        OS.Environment.load_vars(f"{OS.Path.cwd()}/.env")

    def config(self):
        return {
            "objects": ObjectPool(),
            "manifest": self.manifest(),
            "loggers": LoggerPool()
        }

    @resource
    def manifest(self):
        home = OS.Environment.var(Constant.home)
        manifest: Manifest = Manifest.load(home)

        if manifest.api_version != "1":
            raise ValueError(f"Pandora API Version (api_version) '{manifest.api_version}' is not valid. " +
                             f"(App Home: '{home}').")

        ObjectPool().add(key=str(AppEnvironment.oid), obj=manifest.preferences.environment)

        return manifest
