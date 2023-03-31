from typing import List, Optional

from ...commons.serialization import Serializable, YAML
from ...commons.stypes import String


class AppManifest(Serializable):
    name: str = String.EMPTY
    description: str = String.EMPTY
    authors: List[str] = []
    command: str = String.EMPTY
    version: str = String.EMPTY

    def __str__(self):
        cls_template = \
            ":: App '{app_name}' (v{version})\n" \
            ".. Description: {app_desc}\n" \
            ".. Authors: {authors}\n" \
            ".. Command: '{command}'"

        return cls_template.format(app_name=self.name, app_desc=self.description,
                                   version=self.version, authors=self.authors, command=self.command)


class AppPreferences(Serializable):
    command_delay: int
    lang: str
    environment: str

    def __str__(self):
        cls_template = \
            ".. Command Delay: {delay}ms\n" \
            ".. Language: {lang}\n" \
            ".. Environment: '{env}'"

        return cls_template.format(delay=self.command_delay,
                                   lang=self.lang,
                                   env=self.environment)


class Manifest(Serializable):
    api_version: str = String.EMPTY
    app: AppManifest = AppManifest
    preferences: AppPreferences = AppPreferences
    repositories: List[str] = []

    def __init__(self, **entries):
        if entries is not None and len(entries) > 0:
            super().__init__(**entries)

    @staticmethod
    def load(path: str):
        manifest: Optional[Manifest]

        if String.not_empty(path):
            manifest_file: str = "{}/manifest.yml".format(path)
            manifest = YAML.load(manifest_file, Manifest)
        else:
            raise ValueError(f"Manifest File could not be loaded because provided path is empty.")

        return manifest

    @property
    def runtime(self):
        import sys
        return str(sys.version).replace("\n", "")

    def __str__(self):
        template = "{app}\n" \
                   "{preferences}" \
                   ".. Runtime: {runtime}\n" \
                   ".. Pandora API version: {api_version}\n" \
                   ".. Plugin Repositories: {plugins}"

        return template.format(
            app=str(self.app),
            preferences=str(self.preferences),
            runtime=self.runtime,
            api_version=self.api_version,
            plugins=str(self.repositories))
