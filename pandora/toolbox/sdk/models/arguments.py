from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Tuple, Any

from pandora.commons import Collection, String


@dataclass
class PluginRuntimeArguments:
    """
    Abstracts the Plugin Arguments.
    """
    def __init__(self, arguments: List[Tuple[str, Any]]):
        self.__cache: Optional[deque] = None
        self.arguments: List[Tuple[str, Any]] = arguments

    @property
    def additional_args(self) -> List[Tuple[str, Any]]:
        """
        :return: all additional arguments that might exist.
        """
        args_copy = self.arguments.copy()
        args_copy.pop(0)

        return args_copy

    @property
    def main(self) -> str:
        if Collection.not_empty(self.arguments):
            return str(self.arguments[0][1])

    def next(self) -> Tuple[str, Any]:
        if Collection.is_empty(self.__cache):
            self.__cache = deque(self.additional_args.copy())

        return self.__cache.popleft()

    @property
    def is_present(self) -> bool:
        return Collection.not_empty(self.arguments)

    def value(self, arg_name: str) -> Optional[Any]:
        arg_value: Any = None

        if String.not_empty(arg_name):
            for arg in self.arguments:
                if arg[0] == arg_name:
                    arg_value = arg[1]
                    break

        return arg_value
