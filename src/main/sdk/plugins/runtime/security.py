from typing import List

from src.main.commons import String
from src.main.sdk.models.plugin import Plugin


class RuntimeSecurityContainer:
    @staticmethod
    def exec(plugin: Plugin, args: List[str]):
        pass

    @classmethod
    def is_signature_valid(cls, plugin: Plugin = None):
        pass

    @classmethod
    def allow_execution(cls, plugin: Plugin = None):
        dev: str = "dev"
        loaded_env: str = "dev"

        if String.equals(dev, loaded_env):
            # TODO: Place a warning about unsafe code execution
            return True
        else:
            return cls.is_signature_valid(plugin)
