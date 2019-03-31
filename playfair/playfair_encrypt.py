import logging
import re

from playfair.objects import Block
from playfair.objects import Rule

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PlayFairEncrypt(object):
    def __init__(self, playfair_key):
        self._playfair_key = playfair_key

    def encrypt(self, message):
        self._plain_text = message
        self._encrypt()
        return self._cipher_text

    def encrypt_file(self, file):
        self._plain_text = open(file).read()
        self._encrypt()
        return self._cipher_text

    def _encrypt(self):
        self._encrypt_blocks()
        self._construct_cipher_text()
        return self._cipher_text

    def _construct_cipher_text(self):
        self._cipher_text = ""
        for block in self._blocks:
            self._cipher_text += block.text

        return self._cipher_text

    def _encrypt_blocks(self):
        self._blocks = []
        for block in self._iterator():
            # get the rule to use for encryption
            cl0 = self._playfair_key.char_location(block.char(0))
            cl1 = self._playfair_key.char_location(block.char(1))
            if cl0.row == cl1.row and cl0.col != cl1.col:
                rule = Rule.row
            elif cl0.row != cl1.row and cl0.col == cl1.col:
                rule = Rule.col
            else:
                rule = Rule.rect

            # apply the rule and add the processed block to the _blocks array
            rule(self._playfair_key, block)
            self._blocks.append(block)

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
