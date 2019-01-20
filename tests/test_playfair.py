import unittest

from playfair import PlayFair


class TestPlayFair(unittest.TestCase):
    def test_01_create_playfair_instance(self):
        playfair = PlayFair()
        self.assertIsNotNone(playfair)
