import unittest

from playfair.objects import Block


class TestBlock(unittest.TestCase):
    def test_01_create_input_block(self):
        block = Block()
        self.assertIsNotNone(block)
        self.assertEqual(len(block._chars), 0)
        self.assertEqual(len(block._specials), 0)
        self.assertEqual(block._index, 0)

    def test_02_add_char(self):
        block = Block()
        block.add_char("a")
        self.assertEqual(block._index, 1)
        self.assertEqual(block._chars[0].char, "a")
        self.assertEqual(block._chars[0].index, 0)
        self.assertEqual(len(block._specials), 0)

        block.add_char("b")
        # more than 2 chars should raise ValueError
        with self.assertRaises(ValueError):
            block.add_char("c")

    def test_03_add_special(self):
        block = Block()
        block.add_special("!")
        self.assertEqual(block._index, 1)
        self.assertEqual(block._specials[0].char, "!")
        self.assertEqual(block._specials[0].index, 0)
        self.assertEqual(len(block._chars), 0)

    def test_04_add_both(self):
        block = Block()
        block.add_char("a")
        block.add_special("!")
        block.add_char("b")

        self.assertEqual(block._chars[0].char, "a")
        self.assertEqual(block._chars[0].index, 0)
        self.assertEqual(block._specials[0].char, "!")
        self.assertEqual(block._specials[0].index, 1)
        self.assertEqual(block._chars[1].char, "b")
        self.assertEqual(block._chars[1].index, 2)
        self.assertEqual(block._index, 3)

    def test_05_current_char(self):
        block = Block()
        self.assertEqual(block.current_char, None)

        block.add_char("a")
        self.assertEqual(block.current_char, "a")

        block.add_char("b")
        self.assertEqual(block.current_char, None)

    def test_06_ready(self):
        block = Block()
        self.assertFalse(block.ready)

        block.add_char("a")
        self.assertFalse(block.ready)

        block.add_char("b")
        self.assertTrue(block.ready)

        with self.assertRaises(ValueError):
            block.add_char("c")
        # even with an insert exception, block that is ready stays ready
        self.assertTrue(block.ready)

    def test_07_has_content(self):
        block = Block()
        self.assertFalse(block.has_content)

        block = Block()
        block.add_char("a")
        self.assertTrue(block.has_content)

        block = Block()
        block.add_special(".")
        self.assertTrue(block.has_content)

    def test_08_char(self):
        block = Block()
        # block is not yet ready, raises exception
        with self.assertRaises(ValueError):
            block.char(0)

        block.add_char("a")
        block.add_char("b")

        # requesting invalid locations
        with self.assertRaises(ValueError):
            block.char(-1)
        with self.assertRaises(ValueError):
            block.char(2)

        # finally a valid request after block is ready
        self.assertEqual(block.char(0), "a")
        self.assertEqual(block.char(1), "b")

    def test_09_text(self):
        # test 2 char 2 special block
        block = Block()
        block.add_char("a")
        block.add_special(",")
        block.add_char("b")
        block.add_special(".")
        self.assertEqual(block.text, "a,b.")

        # test 2 char block
        block = Block()
        block.add_char("a")
        block.add_char("b")
        self.assertEqual(block.text, "ab")

        # test 2 special block
        block = Block()
        block.add_special("!")
        block.add_special("@")
        self.assertEqual(block.text, "!@")
