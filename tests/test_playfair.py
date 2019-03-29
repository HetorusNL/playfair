import unittest
from unittest.mock import patch

from playfair import PlayFair
from playfair import PlayFairEncrypt


class TestPlayFair(unittest.TestCase):
    def test_01_create_playfair_instance(self):
        playfair = PlayFair()
        self.assertIsNotNone(playfair)

    def test_02_substitute_char(self):
        playfair = PlayFair()

        # ensure that correct functions in PlayFairKey are called
        char = "a"
        playfair.substitute_char = char
        self.assertEqual(playfair._key.substitute_char, char)
        self.assertEqual(playfair.substitute_char, char)

    def test_03_substitute_by(self):
        playfair = PlayFair()

        # ensure that correct functions in PlayFairKey are called
        char = "a"
        playfair.substitute_by = char
        self.assertEqual(playfair._key.substitute_by, char)
        self.assertEqual(playfair.substitute_by, char)

    def test_04_padding_char(self):
        playfair = PlayFair()

        # ensure that correct functions in PlayFairKey are called
        char = "a"
        playfair.padding_char = char
        self.assertEqual(playfair._key.padding_char, char)
        self.assertEqual(playfair.padding_char, char)

    def test_05_generate_key(self):
        playfair = PlayFair()

        # make sure that generate_key returns itself, so it can be chained
        generate_key_result = playfair.generate_key("key")
        self.assertEqual(generate_key_result, playfair)

    def test_06_print_tableau(self):
        playfair = PlayFair()

        # ensure that correct function in PlayFairKey is called
        playfair.generate_key()
        playfair.print_tableau()

    def test_07_ensure_valid_key(self):
        playfair = PlayFair()

        # initially the key is invalid, should raise RuntimeError
        with self.assertRaises(RuntimeError):
            playfair._ensure_valid_key()

        # after a valid key is generated it should run successful
        playfair.generate_key("asdf")
        playfair._ensure_valid_key()

    def test_08_encrypt(self):
        playfair = PlayFair()

        # should call _ensure_valid_key and encrypt in PlayFairEncrypt
        with patch.object(playfair, "_ensure_valid_key") as mock_valid:
            with patch.object(PlayFairEncrypt, "encrypt") as mock_encrypt:
                playfair.encrypt("asdf")

        mock_valid.assert_called_once()
        mock_encrypt.assert_called_once()

    def test_09_encrypt_file(self):
        playfair = PlayFair()

        # should call _ensure_valid_key and encrypt in PlayFairEncrypt
        with patch.object(playfair, "_ensure_valid_key") as mock_valid:
            with patch.object(PlayFairEncrypt, "encrypt_file") as mock_encrypt:
                playfair.encrypt_file("file.txt")

        mock_valid.assert_called_once()
        mock_encrypt.assert_called_once()
