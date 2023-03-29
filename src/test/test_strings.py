import unittest

from src.main.commons.stypes import String


class TestString(unittest.TestCase):
    def test_empty_string(self):
        self.assertEquals(String.EMPTY, "")

    def test_is_empty_method(self):
        self.assertTrue(String.is_empty(""))
        self.assertTrue(String.is_empty(String.EMPTY))
        self.assertTrue(String.is_empty(None))
