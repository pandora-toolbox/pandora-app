from logging import Logger
from typing import List, Optional

from pandora.commons import String, Singleton, Tree
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.models import AppManifest
from pandora.toolbox.sdk.models.plugin import Plugin, PluginCollection, PluginCollections, Plugins
from pandora.toolbox.sdk.pools import inject, LoggerPool
from pandora.toolbox.sdk.services.collectionservice import PluginCollectionService


class PluginDiscoveryService(metaclass=Singleton):

    @classmethod
    @inject
    def scan(cls, pandora_app: AppManifest = None) -> (PluginCollections, Plugins, Tree):
        logger: Logger = LoggerPool.get(cls)

        sources: List[str] = []  # List of paths that contains collections (sources)

        collections: PluginCollections = {}  # it is a dict :)
        plugins: Plugins = {}  # it is also a dict hehe

        logger.debug("Creating Command Tree based on the App Manifest...")
        command_tree: Tree = Tree(pandora_app)

        # Add default collection to sources list if exists
        logger.debug("Adding Home Path and Default Plugin Path as sources...")
        sources.append(Constants.HOME_PATH)
        sources.append(Constants.DEFAULT_PLUGIN_PATH)

        # Add declared collections to sources list
        logger.debug("Adding declared collections as sources...")
        sources.extend(pandora_app.collections)

        # Remove eventual duplicates
        sources = list(set(sources))

        # Load Plugin Repositories as PluginCollection
        logger.debug("Scanning Plugin Sources...")
        for source in sources:
            if String.not_empty(source):
                collection: PluginCollection = PluginCollectionService.scan(source)

                if collection is not None:
                    # Add PluginCollection to collections dict
                    logger.debug(f"Adding Plugin Source located at '{source}' as collection.")
                    if String.equals(source, Constants.DEFAULT_PLUGIN_PATH):
                        key: str = "default"
                    else:
                        key: str = collection.location

                    collections[key] = collection

                    # Build part of the Plugin Tree based on the plugins of the loaded collection
                    logger.debug(f"[Plugin Tree] Incrementing Plugin Tree...")
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
