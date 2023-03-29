import unittest

from ..main.commons.stypes import String
from ..main.commons.design_patterns import ObjectContainer


class TestObjectContainer(unittest.TestCase):
    def test_creation(self):
        container: ObjectContainer = ObjectContainer()

        self.assertTrue(container is not None)
        self.assertDictEqual(container.objects, {})

    def test_add_obj(self):

        container: ObjectContainer = ObjectContainer()
        obj: str = String.random(10)

        container.add(key="generic.key", obj=obj)

        self.assertEqual(container.get("generic.key"), obj)
        container.clear()

    def test_inject(self):
        from ..main.commons.design_patterns.object_container import inject

        @inject
        def injected_method(generic_value: str = None):
            return generic_value

        container: ObjectContainer = ObjectContainer()
        container.add(key="generic_value", obj="generic.object")

        self.assertEquals(injected_method(), "generic.object")
        container.clear()
