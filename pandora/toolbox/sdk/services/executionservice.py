from typing import List

from pandora.toolbox.sdk.models import Command
from pandora.toolbox.sdk.models.plugin import Plugin
from pandora.toolbox.sdk.services.securityservice import RuntimeSecurityContainer


class PluginExecutionRuntime:
    @staticmethod
    def exec(command: Command = None, plugin: Plugin = None, args: List[str] = None):
        if command is None:
            raise RuntimeError(f"Error while trying to execute command: Command is 'None'.")

        if plugin is None:
            raise RuntimeError(f"Error while trying to execute command '{command.name}': Plugin is 'None'.")

        if RuntimeSecurityContainer.allow_execution(command):
            RuntimeSecurityContainer.exec(command, args)
        else:
            raise RuntimeError(f"Execution of command '{command.name}' (from '{plugin.name}') with args {args} was "
                               f"denied.")
