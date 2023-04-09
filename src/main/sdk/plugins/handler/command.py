from typing import List, Callable

from src.main.sdk.plugins.arguments import ArgumentDefinition, PluginRuntimeArguments


class Command:
    def __init__(self, handler: Callable = None, args: List[ArgumentDefinition] = None):
        self.method: Callable = handler
        self.args: List[ArgumentDefinition] = args

    def run(self, args: PluginRuntimeArguments = None):
        if args is not None:
            self.method(args)
        else:
            self.method()
