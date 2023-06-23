import argparse
from typing import List, Optional, Dict

from pandora.commons import Tree
from pandora.toolbox.sdk.models import AppManifest
from pandora.toolbox.sdk.models.command import CommandArgument, ArgumentType, Command
from pandora.toolbox.sdk.models.plugin import Plugin


class CLI:
    def __init__(self, command_tree: Tree):
        self._register_commands(command_tree)

    def _register_commands(self, command_tree: Tree):
        if command_tree is not None:
            subparsers = None

            for node in command_tree.walk_forward():
                command: Command

                # For root node, just create a parser based on the app command, e.g. 'pandora'
                if command_tree.root == node and type(node.data) == AppManifest:
                    manifest: AppManifest = node.data
                    self.parser = argparse.ArgumentParser(prog=manifest.command)

                # For plugin nodes, register the commands
                if type(node.data) == Plugin:
                    plugin: Plugin = node.data

                    # Create a subparser to each plugin
                    subparsers = self.parser.add_subparsers(dest="command_name")

                    # Register the subcommands for each plugin
                    for command in plugin.commands:
                        arg: CommandArgument

                        if command:
                            subparser = subparsers.add_parser(name=command.name, help=command.help)

                            for arg in command.arguments:
                                arg_kwargs: dict[str, object]

                                arg_kwargs = {
                                    "help": arg.help,
                                    "required": arg.required
                                }

                                # Set data type
                                if arg.data_type == ArgumentType.String:
                                    arg_kwargs["type"] = str
                                    arg_kwargs["nargs"] = "?"
                                elif arg.data_type == ArgumentType.Bool:
                                    arg_kwargs["action"] = "store_true"
                                elif arg.data_type == ArgumentType.Integer:
                                    arg_kwargs["type"] = int
                                elif arg.data_type == ArgumentType.Float:
                                    arg_kwargs["type"] = float

                                # Set default value
                                arg_kwargs["default"] = argparse.SUPPRESS

                                subparser.add_argument(*arg.name_or_flags, **arg_kwargs)
        else:
            raise ValueError("Command Tree is 'None'.")

    def parse(self, args: List[str]):
        command_name: Optional[str] = None
        nargs: Optional[Dict[str, object]] = None

        if args and len(args) > 0:
            # workaround to support both command with dashes and with spaces
            if (args[0].rfind("-") == -1) and (args[1].rfind("-") == -1):
                args[0] = f"{args[0] + '-' + args[1]}"
                args.remove(args[1])

            parsed_args = self.parser.parse_args(args=args)

            command_name = parsed_args.command_name
            nargs = vars(parsed_args)
            del nargs["command_name"]

        return command_name, nargs
