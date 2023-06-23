from enum import Enum
from typing import List, Optional

from pandora.commons.serialization import Serializable


class ArgumentType(Enum):
    String = "string"
    Bool = "bool"
    Integer = "int"
    Float = "float"

    @staticmethod
    def get(data_type: str = None):
        from pandora.commons import String

        if String.not_empty(data_type):
            argtype: Optional[ArgumentType] = None

            for argtype in ArgumentType:
                if argtype.value == data_type:
                    return argtype

            if argtype is None:
                raise ValueError("Data Type '{data_type}' does not have an associated ArgumentType enumeration.")


# noinspection PyMissingConstructor
class CommandArgument(Serializable):
    def __init__(self,
                 name: str,
                 short: str = None,
                 help: str = None,
                 required: bool = False,
                 data_type: str = None):
        self.name: str = name
        self.short: str = short
        self.help: str = help
        self.required: bool = required
        self.__data_type: str = data_type

    @property
    def data_type(self):
        return ArgumentType.get(self.__data_type)

    @property
    def name_or_flags(self):
        return [self.name, self.short]


# noinspection PyMissingConstructor
class Command(Serializable):
    def __init__(self,
                 name: str,
                 help: str,
                 handler: str = None,
                 arguments: list = None):
        self.name = name
        self.help: str = help
        # self.handler: Callable = handler
        self.handler: str = handler
        self.arguments: List[CommandArgument] = []

        # Workaround to [Issue #4](https://gitlab.com/dev.artemisia/pandora-toolbox/pandora-app/-/issues/4)
        for arg in arguments:
            self.arguments.append(CommandArgument(**arg))
