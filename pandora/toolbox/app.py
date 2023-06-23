from logging import Logger
from typing import List

from pandora.commons.serialization import Serializable
from pandora.toolbox.sdk.cli.parser import CLI
from pandora.toolbox.sdk.config.appconfig import AppConfiguration
from pandora.toolbox.sdk.models import AppManifest
from pandora.toolbox.sdk.services import PluginService
from pandora.toolbox.sdk.pools import ObjectPool, LoggerPool


class ToolboxApp(Serializable):
    """
    Entrypoint of the entire system.
    """

    manifest: AppManifest = AppManifest
    objects: ObjectPool = ObjectPool
    loggers: LoggerPool = LoggerPool()
    plugins: PluginService = PluginService
    cli: CLI = CLI

    def __init__(self):
        self.logger: Logger = LoggerPool.root()
        self.logger.info("Initializing ToolboxApplication...")

        super().__init__(**AppConfiguration()
                         .begin()
                         .load_envvars()
                         .init_object_pool()
                         .load_app_manifest()
                         .load_plugins()
                         .create_cli()
                         .finish())

    def run(self, args: List[str]) -> object:
        """
        Run a Plugin based in a list of command + arguments.
        """
        command, nargs = self.cli.parse(args)

        return self.plugins.exec(command, nargs)
