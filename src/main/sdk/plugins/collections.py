from typing import Dict

from .handler.command import Command
from ..models.plugin import Plugin
from ...commons import String
from ...commons.integrations import OS


class PluginCollection:
    def __init__(self, location: str = String.EMPTY, remote: str = String.EMPTY):
        self.plugins: dict[str, Plugin] = {}
        self.location: str = location
        self.remote: str = remote

    @staticmethod
    def load(location: str):
        collection: PluginCollection = PluginCollection()

        if String.not_empty(location):
            if location.rfind(".git"):
                # remote repo
                # TODO: Improve loading here
                collection.remote = location
            elif OS.Path.exists(location):
                collection.location = location

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
            raise ValueError(f"Not possible to load plugin since 'path' is empty.")

        return collection

