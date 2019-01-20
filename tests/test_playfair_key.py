import unittest

from playfair import PlayFairKey


class TestPlayFair(unittest.TestCase):
    def test_01_create_playfair_key_instance(self):
        playfair_key = PlayFairKey()
        self.assertIsNotNone(playfair_key)

    def test_02_validate_keying_material(self):
        playfair_key = PlayFairKey()

        # test wrong types supplied to the validate function
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material({})
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material([])
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material(PlayFairKey)

        # empty keying material shouldn't raise exception and return ""
        self.assertEqual(playfair_key._validate_keying_material(""), "")

        # ensure key can only use lowercase letters
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material("1")
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material("A")
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material(".")
        with self.assertRaises(ValueError):
            playfair_key._validate_keying_material("\n")

        self.assertEqual(playfair_key._validate_keying_material("a"), "a")
        self.assertEqual(playfair_key._validate_keying_material("z"), "z")
        letters_and_space = "abcdefghijklmnopqrstuvwxyz "
        letters = "abcdefghiklmnopqrstuvwxyz"  # note, without substitute char
        self.assertEqual(
            playfair_key._validate_keying_material(letters_and_space), letters
        )

    def test_03_generate_key(self):
        playfair_key = PlayFairKey()

        # when invalid keying material supplied, don't set keying material
        with self.assertRaises(ValueError):
            playfair_key.generate_key("Invalid KEY!")
        self.assertIsNone(playfair_key._keying_material)

        # check function sets correct key and keying_material values
        self.assertEqual(playfair_key._keying_material, None)
        playfair_key.generate_key("example key example ij")
        self.assertEqual(playfair_key._keying_material, "examplekeyexamplei")
        self.assertEqual(playfair_key._key, "examplkyibcdfghnoqrstuvwz")

        # check that the tableaus are correct
        tableau_row = [
            ["e", "x", "a", "m", "p"],
            ["l", "k", "y", "i", "b"],
            ["c", "d", "f", "g", "h"],
            ["n", "o", "q", "r", "s"],
            ["t", "u", "v", "w", "z"],
        ]
        self.assertEqual(playfair_key._tableau_row, tableau_row)
        tableau_col = [
            ["e", "l", "c", "n", "t"],
            ["x", "k", "d", "o", "u"],
            ["a", "y", "f", "q", "v"],
            ["m", "i", "g", "r", "w"],
            ["p", "b", "h", "s", "z"],
        ]
        self.assertEqual(playfair_key._tableau_col, tableau_col)

    def test_04_is_single_lowercase_char(self):
        playfair_key = PlayFairKey()

        # supply some in valid chars
        with self.assertRaises(ValueError):
            playfair_key._is_single_lowercase_char("A")
        with self.assertRaises(ValueError):
            playfair_key._is_single_lowercase_char("!")
        with self.assertRaises(ValueError):
            playfair_key._is_single_lowercase_char("1")
        with self.assertRaises(ValueError):
            playfair_key._is_single_lowercase_char("aa")

        # supply some valid chars
        self.assertTrue(playfair_key._is_single_lowercase_char("a"))
        self.assertTrue(playfair_key._is_single_lowercase_char("z"))

    def test_05_substitute_char(self):
        playfair_key = PlayFairKey()

        # get default substitute-char and -by
        default_char = playfair_key.substitute_char
        default_by = playfair_key.substitute_by

        # test invalid substitute_char
        with self.assertRaises(ValueError):
            playfair_key.substitute_char = "A"
        with self.assertRaises(ValueError):
            playfair_key.substitute_char = default_by
        self.assertEqual(playfair_key.substitute_char, default_char)

        # test valid substitute_char
        playfair_key.substitute_char = "a"
        self.assertEqual(playfair_key.substitute_char, "a")

    def test_06_substitute_by(self):
        playfair_key = PlayFairKey()

        # get default substitute-char and -by
        default_char = playfair_key.substitute_char
        default_by = playfair_key.substitute_by

        # test invalid substitute_by
        with self.assertRaises(ValueError):
            playfair_key.substitute_by = "A"
        with self.assertRaises(ValueError):
            playfair_key.substitute_by = default_char
        self.assertEqual(playfair_key.substitute_by, default_by)

        # test valid substitute_char
        playfair_key.substitute_by = "a"
        self.assertEqual(playfair_key.substitute_by, "a")

    def test_07_padding_char(self):
        playfair_key = PlayFairKey()

        # get default padding-char, substitute-char and -by
        default_padding_char = playfair_key.padding_char
        default_char = playfair_key.substitute_char
        default_by = playfair_key.substitute_by

        # test invalid substitute_by
        with self.assertRaises(ValueError):
            playfair_key.padding_char = "A"
        with self.assertRaises(ValueError):
            playfair_key.padding_char = default_char
        with self.assertRaises(ValueError):
            playfair_key.padding_char = default_by
        self.assertEqual(playfair_key.padding_char, default_padding_char)

        # test valid substitute_char
        playfair_key.padding_char = "a"
        self.assertEqual(playfair_key.padding_char, "a")

    def test_08_print_tableau(self):
        playfair_key = PlayFairKey()

        # when generate_key hasn't been called, the tableau can't be printed
        with self.assertRaises(ValueError):
            playfair_key.print_tableau()

        playfair_key.generate_key("")
        playfair_key.print_tableau()
        playfair_key.generate_key("playfair example")
        playfair_key.print_tableau()
