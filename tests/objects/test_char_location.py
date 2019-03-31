import unittest

from playfair.objects import CharLocation


class TestCharLocation(unittest.TestCase):
    def test_01_get_set(self):
        cl = CharLocation()
        self.assertEqual(cl.row, -1)
        self.assertEqual(cl.col, -1)

        cl.row = 1
        cl.col = 2
        self.assertEqual(cl.row, 1)
        self.assertEqual(cl.col, 2)

    def test_02_setter_validation(self):
        cl = CharLocation()

        with self.assertRaises(ValueError):
            cl.row = -1
        with self.assertRaises(ValueError):
            cl.row = 6
        with self.assertRaises(ValueError):
            cl.col = -1
        with self.assertRaises(ValueError):
            cl.col = 6

    def test_03_valid(self):
        cl = CharLocation()
        self.assertEqual(cl.valid, False)

        cl.row = 1
        with self.assertRaises(ValueError):
            cl.col = 6
        self.assertEqual(cl.valid, False)

        cl.col = 1
        self.assertEqual(cl.valid, True)
