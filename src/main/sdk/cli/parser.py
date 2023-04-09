import argparse
from typing import List, Optional, Dict

from src.main.commons import Tree
from src.main.sdk.models.plugin import Plugin
from src.main.sdk.plugins.arguments import ArgumentDefinition
from src.main.sdk.plugins.handler.command import Command


class CLI:
    def __init__(self, command_tree: Tree):
        self.parser = argparse.ArgumentParser()
        self._register_commands(command_tree)

    def _register_commands(self, command_tree: Tree):
        subparsers = self.parser.add_subparsers(dest="command_name")

        if command_tree is not None:
            for node in command_tree.walk_forward():
                command_name: str
                command: Command

                plugin: Plugin = node.data
                subparser = subparsers.add_parser(plugin.name)

                for command_name, command in plugin.commands.items():
                    arg: ArgumentDefinition

                    for arg in command.args:
                        arg_kwargs: dict[str, object]

                        arg_kwargs = {
                            "help": arg.help,
                            "required": arg.required
                        }

                        if arg.action == ArgumentDefinition.Action.StoreString:
                            arg_kwargs["type"] = str
                            arg_kwargs["nargs"] = "?"
                            arg_kwargs["default"] = argparse.SUPPRESS
                        elif arg.action == ArgumentDefinition.Action.StoreBool:
                            arg_kwargs["action"] = "store_true"
                            arg_kwargs["default"] = argparse.SUPPRESS
                        elif arg.action == ArgumentDefinition.Action.StoreNumber:
                            arg_kwargs["type"] = float if "." in arg.help else int
                            arg_kwargs["default"] = argparse.SUPPRESS

                        subparser.add_argument(*arg.name_or_flags, **arg_kwargs)
        else:
            raise ValueError("Command Tree is 'None'.")

    def parse(self, args: List[str]):
        command_name: Optional[str] = None
        nargs: Optional[Dict[str, object]] = None

        if not args and len(args) > 0:
            parsed_args = self.parser.parse_args(args=args)
            nargs = vars(parsed_args)
            del nargs["command_name"]

            command_name = parsed_args.command_name

        return command_name, nargs
