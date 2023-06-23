import inspect
from typing import Optional, Callable

from pandora.commons import String
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.models import Command
from pandora.toolbox.sdk.models.arguments import PluginRuntimeArguments
from pandora.toolbox.sdk.models.plugin import Plugin, Module
from pandora.toolbox.sdk.services.securityservice import RuntimeSecurityContainer


class PluginExecutionRuntime:

    @staticmethod
    def exec(command: Command = None,
             plugin: Plugin = None,
             args: Optional[PluginRuntimeArguments] = None):
        """
        Execute securely a function based on a Plugin, Command and Arg
        """

        def validate_deps():
            if command is None:
                raise RuntimeError(f"Error while trying to execute command: Command is 'None'.")

            if plugin is None:
                raise RuntimeError(f"Error while trying to execute command '{command.name}': Plugin is 'None'.")

        validate_deps()

        if RuntimeSecurityContainer.allow_execution(command):
            handler: Callable = PluginExecutionRuntime.load_module(command, plugin)

            if not args:
                return handler()
            else:
                return handler(args.__dict__)
        else:
            raise RuntimeError(f"Execution of command '{command.name}' (from '{plugin.name}') with args {args} was "
                               f"denied.")

    @staticmethod
    def load_module(command: Command = None, plugin: Plugin = None) -> Callable:
        module: Optional[Module] = None
        handler: Optional[str] = None
        package: Optional[str] = None
        callable_handler: Optional[Callable] = None

        # Find the modules available for the target Plugin
        if command and plugin:
            if String.not_empty(command.handler):
                # get the first part of the handler as the module name
                handler = command.handler.rsplit(sep='.')[-1]
                package = "/".join(command.handler.rsplit(sep='.')[:-1])

                for module in plugin.modules:
                    if module.path == f"{Constants.HOME_PATH}/{package}":
                        break

        # Load the module if it was found
        if module:
            module.load()

            if hasattr(module.namespace, handler):
                # Get callable by iterating over the module members and checkign the one that have the same name
                callable_handler = \
                    [member[1] for member in inspect.getmembers(module.namespace) if member[0] == handler][0]

                # Check if the member is a function
                if not inspect.isfunction(callable_handler):
                    raise ValueError(f"Handler '{handler}' in package '{package}' is not a function!")
        else:
            raise RuntimeError(f"No module found for command '{command.name}'.")

        return callable_handler

