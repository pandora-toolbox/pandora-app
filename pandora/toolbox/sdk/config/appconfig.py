from logging import Logger
from typing import Optional

from pandora.toolbox.sdk.cli.parser import CLI
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.models import AppManifest
from pandora.toolbox.sdk.services import PluginService
from pandora.toolbox.sdk.pools import ObjectPool, LoggerPool
from pandora.toolbox.sdk.services.environments import AppEnvironment


class AppConfiguration:

    def __init__(self):
        self.manifest: Optional[AppManifest] = None
        self.objects: Optional[ObjectPool] = None
        self.plugins: Optional[PluginService] = None
        self.cli: Optional[CLI] = None
        self.__loaded_vars: bool = False
        self.logger: Logger = LoggerPool.root()

    @staticmethod
    def begin():
        return AppConfiguration()

    def load_envvars(self):
        self.logger.info("Loading '.env' file...")

        from dotenv import load_dotenv

        load_dotenv(".env")

        self.__loaded_vars = True
        self.logger.info("'.env' file loaded!")

        return self

    def init_object_pool(self):
        """
        Initialize an ObjectPool by generating a Singleton Object.
        """
        self.logger.info("Initializing ObjectPool...")
        self.objects = ObjectPool()
        self.objects.add(self.objects)

        return self

    def load_app_manifest(self):
        """
        Load the application manifest (app.yml) from Current Working Directory (cwd).
        Depends on Object Pool be initialized.
        """
        def validate_deps():
            if self.objects is None:
                raise RuntimeError("To load an Application Manifest, a initialized ObjectPool is required. "
                                   "ObjectPool is 'None'.")

            # TODO: Improve environment management
            if self.__loaded_vars is False:
                raise RuntimeError("In order to load the Application Manifest, "
                                   "some environment variables needs to be configured.")

        validate_deps()

        home_path: str = Constants.HOME_PATH  # Load Constants
        manifest: AppManifest = AppManifest.load(home_path)  # Load an App Manifest

        if manifest.api_version != "1":
            raise ValueError(f"Pandora API Version (api_version) '{manifest.api_version}' is not valid. " +
                             f"(App Home: '{home_path}').")

        # Add objects to ObjectPool
        self.objects.add(key=AppEnvironment.OID.value, obj=manifest.preferences.environment)
        self.objects.add(manifest)

        # Add manifest to AppConfiguration
        self.manifest = manifest

        return self

    def load_plugins(self):
        """
        Creates a Plugin Container and do a first plugin scan in order to load available plugins.
        """
        self.plugins = PluginService()

        self.plugins.scan()

        return self

    def create_cli(self):
        """
        Create a CLI Object to handles with User Interactions and Inputs.
        Depends on plugins being loaded.
        """
        if not self.plugins.last_scan:
            raise RuntimeError("Impossible to create CLI Object with an empty PluginContainer. "
                               "Please run a scan at least once.")

        self.cli = self.plugins.cli()

        return self

    def finish(self):
        """
        Returns a dictionary with the App Configuration.
        """
        return {
            "objects": self.objects,
            "manifest": self.manifest,
            "plugins": self.plugins,
            "cli": self.cli
        }
