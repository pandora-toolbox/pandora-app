from types import ModuleType
from typing import Optional, Union, Dict, List

from src.main.commons import String, Collection
from src.main.commons.integrations import OS
from src.main.commons.integrations.python.modules import DynamicImport
from src.main.sdk.models import Manifest
from src.main.sdk.plugins.handler.command import Command


class Plugin:

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

        @property
        def plugin(self):
            """
            Pre-load the Python Plugin from Module defined at `handle.py` file.
            :return: Plugin Object if present
            """
            self.namespace = DynamicImport.run_module(path=self.path)
            return self.namespace.resolve_plugin if self.namespace is not None else None

    def __init__(self, path: str):
        if OS.Path.exists(path):
            self.location: str = path
            self.manifest: Manifest = Manifest.load(path)

            if self.manifest is not None:
                self.module: Optional[Plugin.Module] = None

                app_file: str = "{}/plugin.py".format(path)
                if Collection.is_present(OS.Path.files(path), app_file):
                    self.module = Plugin.Module(app_file)
                else:
                    # logging.warning(f"Plugin Path '{path}' does not contain a Plugin Handler.")
                    pass

                if self.module is not None:
                    self.commands: Dict[str, Command] = self.module.Handler.commands()
        else:
            raise ValueError(f"Not possible to load plugin located at '{path}'.")

    @property
    def name(self):
        if String.not_empty(self.manifest.app.name):
            return self.manifest.app.name
        else:
            raise ValueError("Plugin does not have an name.")

    @property
    def command(self):
        return self.manifest.app.command

    def subcommand_exists(self, subcommand: str) -> bool:
        if String.not_empty(subcommand):
            return Collection.is_present(obj=subcommand, collection=self.commands.keys())
