from src.main.commons.integrations import OS
from .components.manifest import Manifest
from ..commons.design_patterns.object_container import ObjectContainer
from ..commons.serialization import Serializable


class PandoraApp(Serializable):
    manifest: Manifest = Manifest
    obj_container: ObjectContainer = ObjectContainer

    def __init__(self):
        super().__init__(**AppRuntimeConfig().config())


class AppRuntimeConfig:
    """
    Configure the application in a Runtime Level, resolving object dependencies, loading environment variables, etc.
    """
    def __init__(self):
        OS.Environment.load_vars(f"{OS.Path.cwd()}/.env")

        self.__app_dict: dict[str, object] = {}
        self.__app_home: str = OS.Environment.var("PANDORA_HOME")

    def config(self):
        self.resolve_object_container() \
            .resolve_app_manifest()

        return self.__app_dict

    def resolve_app_manifest(self):
        manifest: Manifest = Manifest.load(self.__app_home)

        if manifest.api_version != "1":
            raise ValueError(f"Pandora API Version (api_version) '{manifest.api_version}' is not valid. " +
                             f"(App Home: '{self.__app_home}').")

        self.__app_dict["manifest"] = manifest

        print(manifest)

        return self

    def resolve_object_container(self):
        self.__app_dict["obj_container"] = ObjectContainer()

        return self
