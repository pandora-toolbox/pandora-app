from typing import List

from src.main.sdk.models.plugin import Plugin
from src.main.sdk.plugins.runtime.security import RuntimeSecurityContainer


class PluginExecutionRuntime:
    @staticmethod
    def exec(plugin: Plugin = None, args: List[str] = None):
        if plugin is None:
            raise RuntimeError(f"Error while trying to execute command: Plugin is 'None'.")

        if RuntimeSecurityContainer.allow_execution(plugin):
            RuntimeSecurityContainer.exec(plugin, args)
        else:
            raise RuntimeError(f"Execution of command '{plugin.command}' (from '{plugin.name}') with args {args} was denied.")
