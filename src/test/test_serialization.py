import unittest

from src.main.commons.integrations import OS
from src.main.commons.serialization import YAML


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
        from src.main.app.components.manifest import Manifest

        file: str = f"{OS.Environment.var('PANDORA_HOME')}/manifest.yml"
        manifest: Manifest = YAML.load(file, Manifest)

        self.assertTrue(manifest is not None)
        self.assertEqual(manifest.api_version, "1")

    def test_YAML_register(self):
        from src.main.commons.stypes import String
        from src.main.commons.serialization import Serializable
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

