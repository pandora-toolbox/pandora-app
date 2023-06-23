from types import ModuleType
from typing import Optional, Union, Dict, Set, List

from pandora.commons import String
from pandora.commons.integrations import OS
from pandora.commons.integrations.python.modules import DynamicImport
from pandora.toolbox.sdk.models import PluginManifest
from pandora.toolbox.sdk.models.command import Command


class Module:
    """
    Represents and defines a Pandora Toolbox Plugin Module.
    """

    def __init__(self, path: str):
        """
        Plugin Module representation.

        :param path: absolute path as string of the Plugin module.
        """
        self.__name: Optional[str] = None
        self.path: str = path
        self.namespace: Union[ModuleType, None] = None
        self.commands: Dict[str, Command] = {}

    @property
    def name(self) -> str:
        """
        Name of Plugin Module.
        :return:
        """
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """
        Sets a new Plugin Module name.

        :param new_name: non-blank name
        """
        if String.is_empty(new_name):
            raise ValueError("Plugin Module name is blank.")
        else:
            self.__name = new_name

    @property
    def path(self) -> str:
        """
        Plugin Module absolute path as string.
        :return:
        """
        return self.__path

    @path.setter
    def path(self, new_path: str):
        """
        Sets a new Plugin Module path.
        :param new_path: Plugin Module aboslute path as string
        """
        if String.is_empty(new_path):
            raise ValueError(f"Plugin Path of {self.name} is blank.")
        else:
            self.__path = new_path

    def load(self):
        """
        Load the Python Plugin from Module.
        """
        self.namespace = DynamicImport.run_module(path=self.path)
        return self.namespace


class Plugin:
    location: str = None
    __manifest: PluginManifest = None
    modules: Set[Module] = None

    def __init__(self, path: str):
        if OS.Path.exists(path):
            self.location: str = path
            self.__manifest: PluginManifest = PluginManifest.load(path)

            if self.__manifest is None:
                raise ValueError(f"Path '{path}' does not contain a valid Plugin Manifest file.")

            # TODO: add signature validation

            self.modules: Set[Module] = set()

            for file in OS.Path.files(path):
                if file.rfind(".py") >= 0:
                    self.modules.add(Module(path=file))
        else:
            raise ValueError(f"Not possible to load plugin located at '{path}'.")

    @property
    def name(self):
        if String.not_empty(self.__manifest.name):
            return self.__manifest.name
        else:
            raise ValueError("Plugin does not have an name.")

    @property
    def commands(self) -> List[Command]:
        if self.__manifest is None:
            raise ValueError("Plugin Manifest is 'None'.")

        return self.__manifest.commands

    def command(self, name: str) -> Optional[Command]:
        """
        Get a Command Object and it Module Path from the Plugin Command List based on the command name with dashes.

        @return Command Object if there is a command available or else None
        """
        command: Optional[Command] = None

        if String.not_empty(name):
            for command in self.commands:
                if command.name == name:
                    break

        return command



class PluginCollection:
    def __init__(self, location: str = String.EMPTY, remote: str = String.EMPTY):
        self.plugins: dict[str, Plugin] = {}
        self.location: str = location
        self.remote: str = remote


Plugins = Dict[str, Plugin]
PluginCollections = Dict[str, PluginCollection]
