import unittest

from playfair import PlayFairEncrypt
from playfair import PlayFairKey


class TestPlayFairEncrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._playfair_key = PlayFairKey()
        cls._playfair_key.generate_key("asdf")
        # setup the playfair_key class
        cls._playfair_key._substitute_char = "j"
        cls._playfair_key._substitute_by = "i"
        cls._playfair_key._padding_char = "x"

    def test_01_iterator(self):
        playfair_encrypt = PlayFairEncrypt(self._playfair_key)
        # assert simple 1 and 2 blocks
        playfair_encrypt._plain_text = "ab"
        self._assert_block_content(playfair_encrypt, ["ab"])
        playfair_encrypt._plain_text = "abcd"
        self._assert_block_content(playfair_encrypt, ["ab", "cd"])

        # assert substitute_char
        playfair_encrypt._plain_text = "jaaj"
        self._assert_block_content(playfair_encrypt, ["ia", "ai"])

        # assert padding between same chars
        playfair_encrypt._plain_text = "aab"
        self._assert_block_content(playfair_encrypt, ["ax", "ab"])

        # assert padding after un-even characters plain_text
        playfair_encrypt._plain_text = "abc"
        self._assert_block_content(playfair_encrypt, ["ab", "cx"])

        # assert padding after un-even characters plain_text
        playfair_encrypt._plain_text = "a='1'b!c?d"
        self._assert_block_content(playfair_encrypt, ["ab", "cd"])
        blocks = list(playfair_encrypt._iterator())
        for special in blocks[0]._specials:
            print("at index: ", special.index, " is character: ", special.char)
        for char in blocks[0]._chars:
            print("at index: ", char.index, " is character: ", char.char)

    def _assert_block_content(self, playfair_encrypt, correct_blocks):
        blocks = list(playfair_encrypt._iterator())
        self.assertEqual(len(blocks), len(correct_blocks))

        for index in range(len(blocks)):
            block = blocks[index]
            correct_block = correct_blocks[index]

            self.assertEqual(block._chars[0].char, correct_block[0])
            self.assertEqual(block._chars[1].char, correct_block[1])
