import unittest

from playfair.objects import Char


class TestChar(unittest.TestCase):
    def test_01_create_char(self):
        # valid char
        char = Char(0, "a")
        self.assertIsNotNone(char)

        # invalid index
        with self.assertRaises(ValueError):
            Char("0", "a")

        # invalid char
        with self.assertRaises(ValueError):
            Char(0, 1)

    def test_02_get_index(self):
        char = Char(0, "a")
        self.assertEqual(char.index, 0)

    def test_03_get_char(self):
        char = Char(0, "a")
        self.assertEqual(char.char, "a")

    def test_04_char_setter(self):
        char = Char(0, "a")
        char.char = "b"
        self.assertEqual(char.char, "b")
        with self.assertRaises(ValueError):
            char.char = 0

    def test_05_index_setter(self):
        char = Char(0, "a")
        char.index = 1
        self.assertEqual(char.index, 1)
        with self.assertRaises(ValueError):
            char.index = "a"
