from typing import List, Dict, Optional

from src.main.commons import String, Singleton, Tree
from src.main.commons.integrations import OS
from src.main.sdk.models import Manifest, Constants
from src.main.sdk.models.plugin import Plugin
from src.main.sdk.plugins.collections import PluginCollection
from src.main.sdk.pools import inject

Plugins = Dict[str, Plugin]
PluginCollections = Dict[str, PluginCollection]


class PluginDiscoveryService(metaclass=Singleton):
    @classmethod
    @inject
    def scan(cls, pandora_app: Manifest = None) -> (PluginCollections, Plugins, Tree):
        repositories: List[str] = []

        collections: PluginCollections = {}
        plugins: Plugins = {}
        tree: Tree = Tree(Plugin(Constants.home))

        # Add default collection to repositories list if exists
        default_collection_path: str = f"{Constants.home}/data/plugins"
        if OS.Path.exists(default_collection_path):
            repositories.append(default_collection_path)

        # Add declared collections to repositories list
        repositories.extend(pandora_app.collections)

        # Load Plugin Repositories as PluginCollection
        for repo in repositories:
            if String.not_empty(repo):
                collection: PluginCollection = PluginCollection.load(repo)

                if collection is not None:
                    # Add PluginCollection to collections dict
                    if String.equals(repo, default_collection_path):
                        key: str = "default"
                        tree.root.data.commands = {}  # TODO: Force an empty command collection to root
                    else:
                        key: str = collection.location

                    collections[key] = collection

                    # Build part of the Plugin Tree based on the plugins of the loaded collection
                    for collection in collections.values():
                        plugin: Plugin

                        for plugin in collection.plugins:
                            plugins[plugin.command] = plugin
                            tree.add_node(plugin)
            else:
                raise ValueError("An empty Plugin Path was provided in the app configuration.")

        return collections, plugins, tree


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
