import unittest

from playfair.objects import InputBlock


class TestInputBlock(unittest.TestCase):
    def test_01_create_input_block(self):
        input_block = InputBlock()
        self.assertIsNotNone(input_block)
        self.assertEqual(len(input_block._chars), 0)
        self.assertEqual(len(input_block._specials), 0)
        self.assertEqual(input_block._index, 0)

    def test_02_add_char(self):
        input_block = InputBlock()
        input_block.add_char("a")
        self.assertEqual(input_block._index, 1)
        self.assertEqual(input_block._chars[0].char, "a")
        self.assertEqual(input_block._chars[0].index, 0)
        self.assertEqual(len(input_block._specials), 0)

        input_block.add_char("b")
        # more than 2 chars should raise ValueError
        with self.assertRaises(ValueError):
            input_block.add_char("c")

    def test_03_add_special(self):
        input_block = InputBlock()
        input_block.add_special("!")
        self.assertEqual(input_block._index, 1)
        self.assertEqual(input_block._specials[0].char, "!")
        self.assertEqual(input_block._specials[0].index, 0)
        self.assertEqual(len(input_block._chars), 0)

    def test_04_add_both(self):
        input_block = InputBlock()
        input_block.add_char("a")
        input_block.add_special("!")
        input_block.add_char("b")

        self.assertEqual(input_block._chars[0].char, "a")
        self.assertEqual(input_block._chars[0].index, 0)
        self.assertEqual(input_block._specials[0].char, "!")
        self.assertEqual(input_block._specials[0].index, 1)
        self.assertEqual(input_block._chars[1].char, "b")
        self.assertEqual(input_block._chars[1].index, 2)
        self.assertEqual(input_block._index, 3)

    def test_05_current_char(self):
        input_block = InputBlock()
        self.assertEqual(input_block.current_char, None)

        input_block.add_char("a")
        self.assertEqual(input_block.current_char, "a")

        input_block.add_char("b")
        self.assertEqual(input_block.current_char, None)

    def test_06_ready(self):
        input_block = InputBlock()
        self.assertFalse(input_block.ready)

        input_block.add_char("a")
        self.assertFalse(input_block.ready)

        input_block.add_char("b")
        self.assertTrue(input_block.ready)

        with self.assertRaises(ValueError):
            input_block.add_char("c")
        # even with an insert exception, input_block that is ready stays ready
        self.assertTrue(input_block.ready)
