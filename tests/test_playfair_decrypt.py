import unittest
from unittest.mock import patch

from playfair.objects import Block
from playfair import PlayFairDecrypt
from playfair import PlayFairKey


class TestPlayFairDecrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._playfair_key = PlayFairKey()
        cls._playfair_key.generate_key("asdf")
        # setup the playfair_key class
        cls._playfair_key._substitute_char = "j"
        cls._playfair_key._substitute_by = "i"
        cls._playfair_key._padding_char = "x"

    def test_01_iterator(self):
        playfair_decrypt = PlayFairDecrypt(self._playfair_key)
        # assert simple 1 and 2 blocks
        playfair_decrypt._cipher_text = "ab"
        self._assert_block_content(playfair_decrypt, ["ab"])
        playfair_decrypt._cipher_text = "abcd"
        self._assert_block_content(playfair_decrypt, ["ab", "cd"])

        # assert substitute_char
        playfair_decrypt._cipher_text = "iaai"
        self._assert_block_content(playfair_decrypt, ["ia", "ai"])

        # assert padding between same chars
        playfair_decrypt._cipher_text = "axab"
        self._assert_block_content(playfair_decrypt, ["ax", "ab"])

        # assert padding after un-even characters cipher_text
        playfair_decrypt._cipher_text = "abcx"
        self._assert_block_content(playfair_decrypt, ["ab", "cx"])

        # assert padding after un-even characters cipher_text
        playfair_decrypt._cipher_text = "a='1'b!c?d"
        self._assert_block_content(playfair_decrypt, ["ab", "cd"])

        # assert special_chars appended to empty block appear in output
        playfair_decrypt._cipher_text = "ab1337"
        # blocks should contain: [{["ab"],[]}, {[],["1337"]}]
        self._assert_block_content(playfair_decrypt, ["ab", []])
        blocks = list(playfair_decrypt._iterator())
        self.assertTrue(blocks[1].has_content)

    def test_02_decrypt_blocks(self):
        playfair_decrypt = PlayFairDecrypt(self._playfair_key)

        # test row function
        playfair_decrypt._cipher_text = "sd"
        playfair_decrypt._decrypt_blocks()
        block = playfair_decrypt._blocks[0]
        self.assertEqual(block.char(0), "a")
        self.assertEqual(block.char(1), "s")

        # test col function
        playfair_decrypt._cipher_text = "zb"
        playfair_decrypt._decrypt_blocks()
        block = playfair_decrypt._blocks[0]
        self.assertEqual(block.char(0), "u")
        self.assertEqual(block.char(1), "z")

        # test rect function
        playfair_decrypt._cipher_text = "bv"
        playfair_decrypt._decrypt_blocks()
        block = playfair_decrypt._blocks[0]
        self.assertEqual(block.char(0), "a")
        self.assertEqual(block.char(1), "z")

        # test special char block at the end of plain_text should be processed
        playfair_decrypt._cipher_text = "bv1337"
        playfair_decrypt._decrypt_blocks()
        block = playfair_decrypt._blocks[0]
        self.assertEqual(block.char(0), "a")
        self.assertEqual(block.char(1), "z")

    def test_03_construct_cipher_text(self):
        playfair_decrypt = PlayFairDecrypt(self._playfair_key)
        playfair_decrypt._blocks = []

        # add plain block
        block = Block()
        block.add_char("a")
        block.add_char("b")
        playfair_decrypt._blocks.append(block)

        # add block with specials
        block = Block()
        block.add_special(",")
        block.add_char("c")
        block.add_special(".")
        block.add_char("d")
        block.add_special("1")
        playfair_decrypt._blocks.append(block)

        # add blocks with padding chars (foo)
        block = Block()
        block.add_char("f")
        block.add_char("o")
        playfair_decrypt._blocks.append(block)
        block = Block()
        block.add_char("x")
        block.add_char("o")
        playfair_decrypt._blocks.append(block)

        # add block with substitute_by
        block = Block()
        block.add_char("i")
        block.add_char("a")
        playfair_decrypt._blocks.append(block)

        # add block ending with padding_char
        block = Block()
        block.add_char("o")
        block.add_char("x")
        playfair_decrypt._blocks.append(block)

        plain_text = "ab,c.d1foojao"
        self.assertEqual(playfair_decrypt._construct_plain_text(), plain_text)

    def test_04_private_decrypt(self):
        playfair_decrypt = PlayFairDecrypt(self._playfair_key)
        # ensure that the required functions are called
        with patch.object(playfair_decrypt, "_construct_plain_text") as cpt:
            with patch.object(playfair_decrypt, "_decrypt_blocks") as db:
                playfair_decrypt._plain_text = "1337"
                # ensure that the constructed ciphertext is returned
                self.assertEqual(playfair_decrypt._decrypt(), "1337")
                db.assert_called_once()
                cpt.assert_called_once()

    def test_05_decrypt(self):
        playfair_decrypt = PlayFairDecrypt(self._playfair_key)
        cipher_text = "@asdf!"
        plain_text = "plain_text"
        with patch.object(playfair_decrypt, "_decrypt") as _decrypt:
            playfair_decrypt._plain_text = plain_text
            result = playfair_decrypt.decrypt(cipher_text)
            _decrypt.assert_called_once()
            self.assertEqual(playfair_decrypt._cipher_text, cipher_text)
            self.assertEqual(result, plain_text)

    def test_06_decrypt_file(self):
        playfair_decrypt = PlayFairDecrypt(self._playfair_key)
        message = "02_dec_file.txt: cipher text\n"
        cipher_text = "cipher_text"
        filename = "tests/files/02_dec_file.txt"
        with patch.object(playfair_decrypt, "_decrypt") as _decrypt:
            playfair_decrypt._plain_text = cipher_text
            result = playfair_decrypt.decrypt_file(filename)
            _decrypt.assert_called_once()
            self.assertEqual(playfair_decrypt._cipher_text, message)
            self.assertEqual(result, cipher_text)

    def _assert_block_content(self, playfair_decrypt, correct_blocks):
        blocks = list(playfair_decrypt._iterator())
        self.assertEqual(len(blocks), len(correct_blocks))

        for index in range(len(blocks)):
            block = blocks[index]
            correct_block = correct_blocks[index]

            if block.ready:
                self.assertEqual(block.char(0), correct_block[0])
                self.assertEqual(block.char(1), correct_block[1])
