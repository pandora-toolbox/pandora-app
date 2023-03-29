from ..commons.design_patterns.object_container import ObjectContainer
from .components.manifest import Manifest


class AppDependencyResolver:
    @staticmethod
    def app_manifest():
        from ..commons.integrations import OS

        app_home = OS.var("PANDORA_HOME")
        manifest: Manifest = Manifest.load(app_home)

        if manifest.api_version != "1":
            raise ValueError(f"Pandora API Version (api_version) '{manifest.api_version}' is not valid. " +
                             f"(App Home: '{app_home}').")

        return manifest


class PandoraApp:
    def __init__(self):
        self.manifest: Manifest = AppDependencyResolver.app_manifest()
        self.obj_container: ObjectContainer = ObjectContainer()
