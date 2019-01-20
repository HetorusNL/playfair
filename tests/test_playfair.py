import unittest

from playfair import PlayFair


class TestPlayFair(unittest.TestCase):
    def test_01_create_playfair_instance(self):
        playfair = PlayFair()
        self.assertIsNotNone(playfair)

    def test_02_validate_keying_material(self):
        playfair = PlayFair()

        # test wrong types supplied to the validate function
        with self.assertRaises(ValueError):
            playfair._validate_keying_material({})
        with self.assertRaises(ValueError):
            playfair._validate_keying_material([])
        with self.assertRaises(ValueError):
            playfair._validate_keying_material(PlayFair)

        # empty keying material shouldn't raise exception and return ""
        self.assertEqual(playfair._validate_keying_material(""), "")

        # ensure key can only use lowercase letters
        with self.assertRaises(ValueError):
            playfair._validate_keying_material("1")
        with self.assertRaises(ValueError):
            playfair._validate_keying_material("A")
        with self.assertRaises(ValueError):
            playfair._validate_keying_material(".")
        with self.assertRaises(ValueError):
            playfair._validate_keying_material("\n")

        self.assertEqual(playfair._validate_keying_material("a"), "a")
        self.assertEqual(playfair._validate_keying_material("z"), "z")
        letters_and_space = "abcdefghijklmnopqrstuvwxyz "
        letters = "abcdefghiklmnopqrstuvwxyz"  # note, without substitute char
        self.assertEqual(
            playfair._validate_keying_material(letters_and_space), letters
        )

    def test_03_generate_key(self):
        playfair = PlayFair()

        # when invalid keying material supplied, don't set keying material
        with self.assertRaises(ValueError):
            playfair.generate_key("Invalid KEY!")
        self.assertIsNone(playfair._keying_material)

        # check function sets correct key and keying_material values
        self.assertEqual(playfair._keying_material, None)
        playfair.generate_key("example key example ij")
        self.assertEqual(playfair._keying_material, "examplekeyexamplei")
        self.assertEqual(playfair._key, "examplkyibcdfghnoqrstuvwz")

        # check that the tableaus are correct
        tableau_row = [
            ["e", "x", "a", "m", "p"],
            ["l", "k", "y", "i", "b"],
            ["c", "d", "f", "g", "h"],
            ["n", "o", "q", "r", "s"],
            ["t", "u", "v", "w", "z"],
        ]
        self.assertEqual(playfair._tableau_row, tableau_row)
        tableau_col = [
            ["e", "l", "c", "n", "t"],
            ["x", "k", "d", "o", "u"],
            ["a", "y", "f", "q", "v"],
            ["m", "i", "g", "r", "w"],
            ["p", "b", "h", "s", "z"],
        ]
        self.assertEqual(playfair._tableau_col, tableau_col)

    def test_04_is_single_lowercase_char(self):
        playfair = PlayFair()

        # supply some in valid chars
        with self.assertRaises(ValueError):
            playfair._is_single_lowercase_char("A")
        with self.assertRaises(ValueError):
            playfair._is_single_lowercase_char("!")
        with self.assertRaises(ValueError):
            playfair._is_single_lowercase_char("1")
        with self.assertRaises(ValueError):
            playfair._is_single_lowercase_char("aa")

        # supply some valid chars
        self.assertTrue(playfair._is_single_lowercase_char("a"))
        self.assertTrue(playfair._is_single_lowercase_char("z"))

    def test_05_substitute_char(self):
        playfair = PlayFair()

        # get default substitute-char and -by
        default_char = playfair.substitute_char
        default_by = playfair.substitute_by

        # test invalid substitute_char
        with self.assertRaises(ValueError):
            playfair.substitute_char = "A"
        with self.assertRaises(ValueError):
            playfair.substitute_char = default_by
        self.assertEqual(playfair.substitute_char, default_char)

        # test valid substitute_char
        playfair.substitute_char = "a"
        self.assertEqual(playfair.substitute_char, "a")

    def test_06_substitute_by(self):
        playfair = PlayFair()

        # get default substitute-char and -by
        default_char = playfair.substitute_char
        default_by = playfair.substitute_by

        # test invalid substitute_by
        with self.assertRaises(ValueError):
            playfair.substitute_by = "A"
        with self.assertRaises(ValueError):
            playfair.substitute_by = default_char
        self.assertEqual(playfair.substitute_by, default_by)

        # test valid substitute_char
        playfair.substitute_by = "a"
        self.assertEqual(playfair.substitute_by, "a")

    def test_07_padding_char(self):
        playfair = PlayFair()

        # get default padding-char, substitute-char and -by
        default_padding_char = playfair.padding_char
        default_char = playfair.substitute_char
        default_by = playfair.substitute_by

        # test invalid substitute_by
        with self.assertRaises(ValueError):
            playfair.padding_char = "A"
        with self.assertRaises(ValueError):
            playfair.padding_char = default_char
        with self.assertRaises(ValueError):
            playfair.padding_char = default_by
        self.assertEqual(playfair.padding_char, default_padding_char)

        # test valid substitute_char
        playfair.padding_char = "a"
        self.assertEqual(playfair.padding_char, "a")

    def test_08_print_tableau(self):
        playfair = PlayFair()

        # when generate_key hasn't been called, the tableau can't be printed
        with self.assertRaises(ValueError):
            playfair.print_tableau()

        playfair.generate_key()
        playfair.print_tableau()
        playfair.generate_key("playfair example")
        playfair.print_tableau()
