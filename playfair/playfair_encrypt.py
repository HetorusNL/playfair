import logging
import re

from playfair.objects import Block

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PlayFairEncrypt(object):
    def __init__(self, playfair_key):
        self._playfair_key = playfair_key

    def encrypt(self, message):
        self._plain_text = message
        self._encrypt()

    def encrypt_file(self, file):
        self._plain_text = open(file).read()
        self._encrypt()

    def _encrypt(self):
        for block in self._iterator():
            pass

    def _iterator(self):
        block = Block()
        valid_chars = re.compile(r"^[a-z]$")

        for char in self._plain_text:
            if not valid_chars.match(char):
                block.add_special(char)
                continue

            if char == self._playfair_key.substitute_char:
                char = self._playfair_key.substitute_by

            if char == block.current_char:
                block.add_char(self._playfair_key.padding_char)
                yield block
                block = Block()

            block.add_char(char)
            if block.ready:
                yield block
                block = Block()

        if block.current_char:
            block.add_char(self._playfair_key.padding_char)
            yield block
