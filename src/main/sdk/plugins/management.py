from typing import List, Optional

from .runtime.discovery import PluginDiscoveryService, PluginCollections, Plugins
from .runtime.execution import PluginExecutionRuntime
from ..cli.parser import CLI
from ..models.plugin import Plugin
from ...commons import Tree, String


class PluginContainer:
    collections: PluginCollections
    plugins: Plugins
    cmd_tree: Tree

    def __init__(self):
        self.collections, self.plugins, self.cmd_tree = PluginDiscoveryService.scan()

        if self.cmd_tree is not None:
            self.CLI = CLI(self.cmd_tree)
        else:
            raise ValueError("Not possible to parse Plugins into CLI interface since Plugin Command Tree is 'None'.")

    def exec(self, command: str, args: List[str]) -> Optional[object]:
        # output = None
        output = self.collections

        if String.not_empty(command) and args is not None:
            plugin: Plugin = self.get(command, args)

            # output = PluginExecutionRuntime.exec(plugin, args)

        return output

    def get(self, cmd_name, provided_args) -> Optional[Plugin]:
        from src.main.commons import Node

        plugin: Optional[Plugin] = None
        node: Node
        for node in self.cmd_tree.walk_forward():
            if node.data.name == cmd_name:
                for arg in provided_args:
                    if arg in node.data.commands:
                        plugin = node.data

        return plugin
