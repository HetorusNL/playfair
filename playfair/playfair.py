import logging

from .playfair_decrypt import PlayFairDecrypt
from .playfair_encrypt import PlayFairEncrypt
from .playfair_key import PlayFairKey

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PlayFair(object):
    def __init__(self):
        # the key properties and calculations happen in PlayFairKey
        self._key = PlayFairKey()

    # get and set properties used by the PlayFairKey
    @property
    def substitute_char(self):
        return self._key.substitute_char

    @substitute_char.setter
    def substitute_char(self, char):
        self._key.substitute_char = char

    @property
    def substitute_by(self):
        return self._key.substitute_by

    @substitute_by.setter
    def substitute_by(self, char):
        self._key.substitute_by = char

    @property
    def padding_char(self):
        return self._key.padding_char

    @padding_char.setter
    def padding_char(self, char):
        self._key.padding_char = char

    # called with the keying_material to generate the PlayFair key
    def generate_key(self, keying_material=""):
        self._key.generate_key(keying_material)
        return self

    # print the tableau after the keying_material is parsed and key generated
    def print_tableau(self):
        self._key.print_tableau()

    # encrypt functions
    def encrypt(self, message):
        self._ensure_valid_key()

        playfair_encrypt = PlayFairEncrypt(self._key)
        ciphertext = playfair_encrypt.encrypt(message)
        return ciphertext

    def encrypt_file(self, file):
        self._ensure_valid_key()

        playfair_encrypt = PlayFairEncrypt(self._key)
        ciphertext = playfair_encrypt.encrypt_file(file)
        return ciphertext

    # decrypt functions
    def decrypt(self, cipher_text):
        self._ensure_valid_key()

        playfair_decrypt = PlayFairDecrypt(self._key)
        plain_text = playfair_decrypt.decrypt(cipher_text)
        return plain_text

    def decrypt_file(self, file):
        self._ensure_valid_key()

        playfair_decrypt = PlayFairDecrypt(self._key)
        plain_text = playfair_decrypt.decrypt_file(file)
        return plain_text

    # private function to validate that a valid key is available
    def _ensure_valid_key(self):
        if not self._key.valid:
            msg = "No valid key, call generate_key before encrypt or decrypt!"
            raise RuntimeError(msg)
