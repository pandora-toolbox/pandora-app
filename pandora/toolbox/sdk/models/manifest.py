from logging import Logger
from typing import List, Optional

from pandora.commons import OS
from pandora.commons.serialization import Serializable, YAML
from pandora.commons.stypes import String
from pandora.toolbox.sdk.models.command import Command


class AppPreferences(Serializable):
    command_delay: int
    lang: str
    environment: str


# noinspection PyArgumentList
class AppManifest(Serializable):
    api_version: str = String.EMPTY
    name: str = String.EMPTY
    description: str = String.EMPTY
    authors: List[str] = []
    command: str = String.EMPTY
    version: str = String.EMPTY
    subcommands: List[Command] = []
    preferences: AppPreferences = AppPreferences
    collections: List[str] = []

    def __init__(self, **entries):
        if entries is not None and len(entries) > 0:
            super().__init__(**entries)

    @staticmethod
    def load(path: str):
        manifest: Optional[AppManifest]

        if String.not_empty(path):
            manifest_file: str = "{}/app.yml".format(path)
            manifest = YAML.load(manifest_file, AppManifest)
        else:
            raise ValueError(f"Manifest File could not be loaded because provided path is empty.")

        return manifest

    @property
    def runtime(self):
        import sys
        return str(sys.version).replace("\n", "")

    def __str__(self):
        template = "\n" \
                   ":: App '{app_name}' (v{version})\n" \
                   ".. Description: {app_desc}\n" \
                   ".. Authors: {authors}\n" \
                   ".. Command: '{command}'" \
                   ".. Command Delay: {delay}ms\n" \
                   ".. Language: {lang}\n" \
                   ".. Environment: '{env}'" \
                   ".. Runtime: {runtime}\n" \
                   ".. Pandora API version: {api_version}\n" \
                   ".. Plugin Collections: {plugins}"

        return template.format(
            app_name=self.name,
            app_desc=self.description,
            version=self.version,
            authors=self.authors,
            command=self.command,
            delay=self.preferences.command_delay,
            lang=self.preferences.lang,
            env=self.preferences.environment,
            runtime=self.runtime,
            api_version=self.api_version,
            plugins=str(self.collections))


# noinspection PyArgumentList
class PluginManifest(Serializable):
    api_version: str = String.EMPTY
    name: str = String.EMPTY
    description: str = String.EMPTY
    authors: List[str] = []
    version: str = String.EMPTY
    commands: List[Command] = []

    def __init__(self, **entries):
        self.__commands = {}
        if entries is not None and len(entries) > 0:
            super().__init__(**entries)

    @staticmethod
    def load(path: str):
        from pandora.toolbox.sdk.pools import LoggerPool  # Avoid circular import

        logger: Logger = LoggerPool.get(name="PluginManifest")

        manifest: Optional[PluginManifest] = None

        if String.not_empty(path):
            manifest_file: str = "{}/commands.yml".format(path)
            logger.debug(f"Checking if there is a Plugin Command Manifest at '{path}'.")

            if OS.Path.exists(manifest_file):
                manifest = YAML.load(manifest_file, PluginManifest)

                logger.debug(f"Plugin Manifest for '{manifest.name}' loaded!")
            else:
                logger.debug(f"No Plugin available at '{path}'.")
        else:
            raise ValueError(f"Plugin Manifest File could not be loaded because provided path is empty.")

        if manifest is not None:
            # Workaround to [Issue #4](https://gitlab.com/dev.artemisia/pandora-toolbox/pandora-app/-/issues/4)
            manifest.__commands = manifest.commands
            manifest.commands = []

            for cmd in manifest.__commands:
                manifest.commands.append(Command(**cmd))

        return manifest

    def __str__(self):
        return None
