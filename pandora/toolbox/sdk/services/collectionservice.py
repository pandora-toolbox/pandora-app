from logging import Logger
from typing import Optional

from pandora.commons import OS
from pandora.commons import String
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.models.plugin import Plugin, PluginCollection
from pandora.toolbox.sdk.pools import LoggerPool


class PluginCollectionService:
    @classmethod
    def load(cls, location: str) -> Optional[PluginCollection]:
        collection: Optional[PluginCollection] = PluginCollection()
        logger: Logger = LoggerPool.get(cls)

        if String.not_empty(location):
            if location.rfind("^.git$") >= 0:
                # remote repo
                # TODO: Improve loading here
                collection.remote = location
            elif OS.Path.exists(location):
                collection.location = location

                # If the Collection Path is the Plugin Home, just load it :)
                if location == Constants.HOME_PATH:
                    try:
                        plugin: Plugin = Plugin(location)
                        collection.plugins[plugin.name] = plugin
                    except ValueError:
                        logger.info("Plugin is not self-contained, so there is no command-as-plugin to add.")
                else:
                    # Load plugins in each subdir
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
            logger.warning(f"Not possible to load plugin since 'path' is empty.")

        return collection
