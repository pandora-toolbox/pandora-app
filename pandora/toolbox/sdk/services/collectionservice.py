from logging import Logger
from typing import Optional

from pandora.commons import OS, Singleton
from pandora.commons import String
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.models.plugin import Plugin, PluginCollection
from pandora.toolbox.sdk.pools import LoggerPool


class PluginCollectionService(metaclass=Singleton):
    @classmethod
    def scan(cls, location: str) -> Optional[PluginCollection]:
        logger: Logger = LoggerPool.get(cls)
        collection: Optional[PluginCollection] = None

        if String.not_empty(location):
            logger.debug(f"Scanning source at '{location}'...")

            if location.rfind("^.git$") >= 0:
                # remote repo
                # TODO: Improve loading here
                collection.remote = location
            elif OS.Path.exists(location):
                collection = PluginCollection()
                collection.location = location

                # If the Collection Path is the Plugin Home, just load it :)
                if location == Constants.HOME_PATH:
                    logger.debug("Target Source is App Home! Checking if the app is a self-contained Plugin...")

                    try:
                        plugin: Plugin = Plugin(location)
                        collection.plugins[plugin.name] = plugin
                    except ValueError:
                        logger.debug("App is not a self-contained Plugin, so there is no command-as-plugin to add.")
                else:
                    # Load plugins in each subdir
                    logger.debug("Scanning sub-dirs...")

                    collection = PluginCollection()

                    for subdir in OS.Path.subdirs(location):
                        if String.not_empty(subdir):
                            plugin: Plugin = Plugin(subdir)
                            collection.plugins[plugin.name] = plugin
                        else:
                            raise ValueError(f"Not possible to load plugin located at '{subdir}'.")
            else:
                raise ValueError(f"Location '{location}' is not a remote neither a local repository.")
        else:
            collection = None
            logger.warning(f"Not possible to scan source collection since 'path' is empty.")

        if len(collection.plugins.keys()) == 0:
            collection = None

        return collection
