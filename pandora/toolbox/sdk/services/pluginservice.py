from datetime import datetime
from typing import List, Optional

from pandora.commons import Tree, String
from pandora.toolbox.sdk.cli.parser import CLI
from pandora.toolbox.sdk.models import Command
from pandora.toolbox.sdk.models.plugin import Plugin, PluginCollections, Plugins
from pandora.toolbox.sdk.services import PluginDiscoveryService
from pandora.toolbox.sdk.services import PluginExecutionRuntime


class PluginService:
    collections: Optional[PluginCollections]
    plugins: Optional[Plugins]
    cmd_tree: Optional[Tree]
    last_scan: Optional[datetime]

    def __init__(self):
        self.collections = None
        self.plugins = None
        self.cmd_tree = None
        self.last_scan = None

    def scan(self):
        """
        Scan Plugin Collections using PluginDiscoveryService and register the available Plugins.
        """
        self.last_scan = datetime.now()
        self.collections, self.plugins, self.cmd_tree = PluginDiscoveryService.scan()

    def cli(self) -> CLI:
        if self.cmd_tree is not None:
            return CLI(self.cmd_tree)
        else:
            raise ValueError("Not possible to parse Plugins into CLI interface since Plugin Command Tree is 'None'.")

    def exec(self, cmd_name: str, args: List[str]) -> Optional[object]:
        # output = None
        output = self.collections

        if String.not_empty(cmd_name):
            command: Optional[Command]
            plugin: Optional[Plugin]

            command, plugin = self.get(cmd_name)

            output = PluginExecutionRuntime.exec(command, plugin, args)

        return output

    def get(self, cmd_name) -> (Optional[Command], Optional[Plugin]):
        """
        Get a plugin based on a command name.
        """
        from pandora.commons.stypes.collections.tree import Node

        node: Node
        plugin: Plugin

        for node in self.cmd_tree.walk_forward():
            if node and type(node.data) == Plugin:
                plugin = node.data

                return plugin.command(cmd_name), plugin

        return None
