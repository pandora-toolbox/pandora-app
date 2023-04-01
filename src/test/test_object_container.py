import unittest

from ..main.commons.stypes import String
from ..main.commons.design_patterns import ObjectPool


class TestObjectContainer(unittest.TestCase):
    def test_creation(self):
        container: ObjectPool = ObjectPool()

        self.assertTrue(container is not None)
        self.assertDictEqual(container.loggers, {})

    def test_add_obj(self):

        container: ObjectPool = ObjectPool()
        obj: str = String.random(10)

        container.add(key="generic.key", obj=obj)

        self.assertEqual(container.get("generic.key"), obj)
        container.clear()

    def test_inject(self):
        from src.main.sdk.components.object_pool import inject

        @inject
        def injected_method(generic_value: str = None):
            return generic_value

        container: ObjectPool = ObjectPool()
        container.add(key="generic_value", obj="generic.object")

        self.assertEquals(injected_method(), "generic.object")
        container.clear()
