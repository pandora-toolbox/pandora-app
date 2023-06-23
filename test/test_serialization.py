import unittest

from main import OS
from pandora.commons.serialization import YAML


class TestYAMLSerialization(unittest.TestCase):
    def test_YAML_generic_deserialization(self):
        file: str = f"{OS.Environment.var('PANDORA_HOME')}/src/test/resources/test.yml"
        generic_obj = YAML.load(file)

        self.assertTrue(generic_obj is not None)
        self.assertEqual(generic_obj.g_str, "generic string")
        self.assertEqual(generic_obj.g_quoted_str, "generic quoted string")
        self.assertEqual(generic_obj.g_int, 1)
        self.assertEqual(generic_obj.g_float, 1.2)

    def test_YAML_class_deserialization(self):
        from pandora.toolbox.sdk.models.manifest import AppManifest

        file: str = f"{OS.Environment.var('PANDORA_HOME')}/manifest.yml"
        manifest: AppManifest = YAML.load(file, AppManifest)

        self.assertTrue(manifest is not None)
        self.assertEqual(manifest.api_version, "1")

    def test_YAML_register(self):
        from pandora.commons.stypes import String
        from pandora.commons.serialization import Serializable
        from io import StringIO

        @YAML.object
        class DumbClass(Serializable):
            def __init__(self, **entries):
                if entries is not None and len(entries) > 0:
                    super().__init__(**entries)
                else:
                    self.attr = String.random(10)

        stream: StringIO = StringIO()

        dumb_class = DumbClass()
        YAML.dump(dumb_class, stream)

        loaded_dumb_class = YAML.load_str(stream.getvalue(), DumbClass)

        self.assertEqual(type(dumb_class), DumbClass)
        self.assertEqual(type(loaded_dumb_class), DumbClass)
        self.assertEqual(dumb_class.attr, loaded_dumb_class.attr)

