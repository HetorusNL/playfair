import unittest
from unittest.mock import patch

from playfair.objects import Block
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

        # assert special_chars appended to empty block appear in output
        playfair_encrypt._plain_text = "ab1337"
        # blocks should contain: [{["ab"],[]}, {[],["1337"]}]
        self._assert_block_content(playfair_encrypt, ["ab", []])
        blocks = list(playfair_encrypt._iterator())
        self.assertTrue(blocks[1].has_content)

    def test_02_encrypt_blocks(self):
        playfair_encrypt = PlayFairEncrypt(self._playfair_key)

        # test row function
        playfair_encrypt._plain_text = "as"
        playfair_encrypt._encrypt_blocks()
        block = playfair_encrypt._blocks[0]
        self.assertEqual(block.char(0), "s")
        self.assertEqual(block.char(1), "d")

        # test col function
        playfair_encrypt._plain_text = "uz"
        playfair_encrypt._encrypt_blocks()
        block = playfair_encrypt._blocks[0]
        self.assertEqual(block.char(0), "z")
        self.assertEqual(block.char(1), "b")

        # test rect function
        playfair_encrypt._plain_text = "az"
        playfair_encrypt._encrypt_blocks()
        block = playfair_encrypt._blocks[0]
        self.assertEqual(block.char(0), "b")
        self.assertEqual(block.char(1), "v")

        # test special char block at the end of plain_text should be processed
        playfair_encrypt._plain_text = "az1337"
        playfair_encrypt._encrypt_blocks()
        block = playfair_encrypt._blocks[0]
        self.assertEqual(block.char(0), "b")
        self.assertEqual(block.char(1), "v")

    def test_03_construct_cipher_text(self):
        playfair_encrypt = PlayFairEncrypt(self._playfair_key)
        playfair_encrypt._blocks = []

        block = Block()
        block.add_char("a")
        block.add_char("b")
        playfair_encrypt._blocks.append(block)

        block = Block()
        block.add_special(",")
        block.add_char("c")
        block.add_special(".")
        block.add_char("d")
        block.add_special("1")
        playfair_encrypt._blocks.append(block)

        self.assertEqual(playfair_encrypt._construct_cipher_text(), "ab,c.d1")

    def test_04_private_encrypt(self):
        playfair_encrypt = PlayFairEncrypt(self._playfair_key)
        # ensure that the required functions are called
        with patch.object(playfair_encrypt, "_construct_cipher_text") as cct:
            with patch.object(playfair_encrypt, "_encrypt_blocks") as meb:
                playfair_encrypt._cipher_text = "1337"
                # ensure that the constructed ciphertext is returned
                self.assertEqual(playfair_encrypt._encrypt(), "1337")
                meb.assert_called_once()
                cct.assert_called_once()

    def test_05_encrypt(self):
        playfair_encrypt = PlayFairEncrypt(self._playfair_key)
        message = "@asdf!"
        cipher_text = "cipher_text"
        with patch.object(playfair_encrypt, "_encrypt") as _encrypt:
            playfair_encrypt._cipher_text = cipher_text
            result = playfair_encrypt.encrypt(message)
            _encrypt.assert_called_once()
            self.assertEqual(playfair_encrypt._plain_text, message)
            self.assertEqual(result, cipher_text)

    def test_06_encrypt_file(self):
        playfair_encrypt = PlayFairEncrypt(self._playfair_key)
        message = "01_enc_file.txt: testmessage\n"
        cipher_text = "cipher_text"
        filename = "tests/files/01_enc_file.txt"
        with patch.object(playfair_encrypt, "_encrypt") as _encrypt:
            playfair_encrypt._cipher_text = cipher_text
            result = playfair_encrypt.encrypt_file(filename)
            _encrypt.assert_called_once()
            self.assertEqual(playfair_encrypt._plain_text, message)
            self.assertEqual(result, cipher_text)

        self.assertEqual(playfair_encrypt._plain_text, message)

    def _assert_block_content(self, playfair_encrypt, correct_blocks):
        blocks = list(playfair_encrypt._iterator())
        self.assertEqual(len(blocks), len(correct_blocks))

        for index in range(len(blocks)):
            block = blocks[index]
            correct_block = correct_blocks[index]

            if block.ready:
                self.assertEqual(block.char(0), correct_block[0])
                self.assertEqual(block.char(1), correct_block[1])
