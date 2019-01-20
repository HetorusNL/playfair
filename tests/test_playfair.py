import unittest

from playfair import PlayFair


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
