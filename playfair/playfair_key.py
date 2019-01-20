import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PlayFairKey(object):
    def __init__(self):
        # store the keying material (passphrase) and key itself
        self._keying_material = None
        self._key = None

        # store the tableau in some different formats
        self._tableau_row = None
        self._tableau_col = None

        # the padding character that will be used inbetween double letters
        self._padding_char = "x"

        # the letter (char) that is substituted by another
        self._substitute_char = "j"
        self._substitute_by = "i"

    @property
    def substitute_char(self):
        return self._substitute_char

    @substitute_char.setter
    def substitute_char(self, char):
        self._is_single_lowercase_char(char)

        # check that both chars aren't the same
        if self.substitute_by == char:
            raise ValueError("Substitute-char and -by can't be the same!")

        self._substitute_char = char

    @property
    def substitute_by(self):
        return self._substitute_by

    @substitute_by.setter
    def substitute_by(self, char):
        self._is_single_lowercase_char(char)

        # check that both chars aren't the same
        if self.substitute_char == char:
            raise ValueError("Substitute-char and -by can't be the same!")

        self._substitute_by = char

    @property
    def padding_char(self):
        return self._padding_char

    @padding_char.setter
    def padding_char(self, char):
        self._is_single_lowercase_char(char)

        # padding-char cannot be the same as substitute-char and -by
        if self.substitute_char == char or self.substitute_by == char:
            raise ValueError(
                "padding-char cannot be the same as as substitute-char ({}) or"
                " -by ({})!".format(self.substitute_char, self.substitute_by)
            )

        self._padding_char = char

    def _is_single_lowercase_char(self, char):
        if not re.match(r"^[a-z]$", char):
            raise ValueError("A single lowercase letter must be suplied!")

        return True

    def generate_key(self, keying_material):
        # validate and set the keying material
        keying_material = self._validate_keying_material(keying_material)
        self._keying_material = keying_material

        # generate alphabet
        regex = r"[{}]".format(self._substitute_char)
        alphabet = re.sub(regex, "", "abcdefghijklmnopqrstuvwxyz")

        # resulting key
        key = ""
        # loop through the keying material, adding letters if not present yet
        for letter in keying_material:
            if letter not in key:
                key += letter

        # loop through the alphabet, adding letters if not present yet
        for letter in alphabet:
            if letter not in key:
                key += letter

        # store the key and initialize the tableaus
        self._key = key
        self._tableau_row = [[] for i in range(5)]
        self._tableau_col = [[] for i in range(5)]

        # fill the correct character in the correct tableau
        for index in range(len(key)):
            self._tableau_row[int(index / 5)] += key[index]
            self._tableau_col[index % 5] += key[index]

    def _validate_keying_material(self, keying_material):
        # check if the keying material is of the correct type (str)
        if type(keying_material) != str:
            raise ValueError("Key must be a str!")

        # check for empty keying_material, if so, log warning but return True
        if len(keying_material) == 0:
            logger.warning("Empty key provided!")
            return keying_material

        # check for correct characters in the keying material
        if not re.match(r"^[a-z ]+$", keying_material):
            raise ValueError(
                "Only lowercase letters and spaces can be supplied as key!"
            )

        # all checks passed,
        # return keying_material with spaces and substitute char removed
        regex = r"[ {}]+".format(self._substitute_char)
        return re.sub(regex, "", keying_material)

    def print_tableau(self):
        if self._tableau_row is None or self._tableau_col is None:
            raise ValueError("No key is present, so can't show tableau!")

        for row in self._tableau_row:
            print("-" * 21)
            for char in row:
                print("| {} ".format(char), end="")
            print("|")
        print("-" * 21)
