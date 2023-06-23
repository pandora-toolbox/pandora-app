from datetime import datetime
from typing import List, Optional

from pandora.commons import String, Singleton, Tree
from pandora.commons.integrations import OS
from pandora.toolbox.sdk.models import AppManifest
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.models.plugin import Plugin, PluginCollection, PluginCollections, Plugins
from pandora.toolbox.sdk.pools import inject
from pandora.toolbox.sdk.services.collectionservice import PluginCollectionService


class PluginDiscoveryService(metaclass=Singleton):
    last_scan: Optional[datetime]

    @classmethod
    @inject
    def scan(cls, pandora_app: AppManifest = None) -> (PluginCollections, Plugins, Tree):
        repositories: List[str] = []  # List of paths that contains collections (repositories)

        collections: PluginCollections = {}  # it is a dict :)
        plugins: Plugins = {}  # it is also a dict hehe
        command_tree: Tree = Tree(pandora_app)

        cls.last_scan = datetime.now()

        # Add default collection to repositories list if exists
        repositories.append(Constants.HOME_PATH)
        repositories.append(Constants.DEFAULT_PLUGIN_PATH)

        # Add declared collections to repositories list
        repositories.extend(pandora_app.collections)
        repositories = list(set(repositories))

        # Load Plugin Repositories as PluginCollection
        for repo in repositories:
            if String.not_empty(repo):
                collection: PluginCollection = PluginCollectionService.load(repo)

                if collection is not None:
                    # Add PluginCollection to collections dict
                    if String.equals(repo, Constants.DEFAULT_PLUGIN_PATH):
                        key: str = "default"
                    else:
                        key: str = collection.location

                    collections[key] = collection

                    # Build part of the Plugin Tree based on the plugins of the loaded collection
                    for collection in collections.values():
                        plugin: Plugin

                        for plugin in collection.plugins.values():
                            plugins[plugin.name] = plugin
                            command_tree.add_node(plugin)
            else:
                raise ValueError("An empty Plugin Path was provided in the app configuration.")

        return collections, plugins, command_tree


    @classmethod
    def get(cls, command: str = None, args: List[str] = None) -> Optional[Plugin]:
    #     if String.not_empty(command):
    #         tree: dict = cls.command_tree()
    #         plugin: Plugin
    #
    #         for plugin in tree.values():
    #             if String.equals(plugin.command, command) and plugin.subcommand_exists(args[0]):
    #                 return plugin
    #
        return None
