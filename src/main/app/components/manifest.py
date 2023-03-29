import sys
from typing import List, Optional

from ...commons.stypes import String
from ...commons.serialization import Serializable, YAML


class AppManifest(Serializable):
    __instance = None
    __root_dir: str = None

    name: String = String()
    description: String = String()
    authors: List[String] = String()
    command: String = String()
    version: String = String()

    def __str__(self):
        cls_template = \
            ".-== [ {app_name} v{version} ] ==-.\n" \
            "~~ {app_desc}\n\n" \
            ":: Authors: {authors}\n" \
            ":: Runtime: Python {runtime_version}"

        return cls_template.format(app_name=self.name, app_desc=self.description,
                                   version=self.version, authors=self.authors,
                                   runtime_version=str(sys.version).replace("\n", ""))


class AppPreferences(Serializable):
    pass


class Manifest(Serializable):
    api_version: str
    app: AppManifest
    preferences: AppPreferences

    @staticmethod
    def load(path: str):
        manifest: Optional[Manifest]

        if String.not_empty(path):
            manifest_file: str = "{}/manifest.yml".format(path)
            manifest = YAML.deserialize(manifest_file, Manifest)
        else:
            raise ValueError(f"Manifest File could not be loaded because provided path is empty.")

        return manifest

    def __str__(self):
        return str(self.__dict__)
