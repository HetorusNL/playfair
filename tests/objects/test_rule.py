import unittest

from playfair import PlayFairKey
from playfair.objects import Block
from playfair.objects import Rule


class TestRule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playfair_key = PlayFairKey()
        cls.playfair_key.generate_key("abcde")

    def test_01_row(self):
        block = Block()
        block.add_char("d")
        block.add_char("e")

        # test increment and roll over
        Rule.row(self.playfair_key, block, Rule.ENCRYPT)
        self.assertEqual(block.char(0), "e")
        self.assertEqual(block.char(1), "a")

        # test increment and roll over
        Rule.row(self.playfair_key, block, Rule.DECRYPT)
        self.assertEqual(block.char(0), "d")
        self.assertEqual(block.char(1), "e")

    def test_02_col(self):
        block = Block()
        block.add_char("s")
        block.add_char("x")

        # test increment and roll over
        Rule.col(self.playfair_key, block, Rule.ENCRYPT)
        self.assertEqual(block.char(0), "x")
        self.assertEqual(block.char(1), "c")

        # test increment and roll over
        Rule.col(self.playfair_key, block, Rule.DECRYPT)
        self.assertEqual(block.char(0), "s")
        self.assertEqual(block.char(1), "x")

    def test_03_rect(self):
        block = Block()
        block.add_char("i")
        block.add_char("r")

        # test rect function
        Rule.rect(self.playfair_key, block, Rule.ENCRYPT)
        self.assertEqual(block.char(0), "g")
        self.assertEqual(block.char(1), "t")

        # test rect function
        Rule.rect(self.playfair_key, block, Rule.DECRYPT)
        self.assertEqual(block.char(0), "i")
        self.assertEqual(block.char(1), "r")

        block = Block()
        block.add_char("w")
        block.add_char("e")

        # test rect function
        Rule.rect(self.playfair_key, block, Rule.ENCRYPT)
        self.assertEqual(block.char(0), "z")
        self.assertEqual(block.char(1), "b")

        # test rect function
        Rule.rect(self.playfair_key, block, Rule.DECRYPT)
        self.assertEqual(block.char(0), "w")
        self.assertEqual(block.char(1), "e")
