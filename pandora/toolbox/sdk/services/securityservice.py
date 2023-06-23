from typing import List

from pandora.commons import String
from pandora.toolbox.sdk.models import Command
from pandora.toolbox.sdk.models.plugin import Plugin


class RuntimeSecurityContainer:
    @staticmethod
    def exec(command: Command, args: List[str]):
        pass

    @classmethod
    def is_signature_valid(cls, plugin: Plugin = None):
        pass

    @classmethod
    def allow_execution(cls, command: Command = None):
        dev: str = "dev"
        loaded_env: str = "dev"

        if String.equals(dev, loaded_env):
            # TODO: Place a warning about unsafe code execution
            return True
        else:
            return cls.is_signature_valid(command)
