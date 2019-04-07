import logging
import re

from playfair.objects import Block
from playfair.objects import Rule

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PlayFairDecrypt(object):
    def __init__(self, playfair_key):
        self._playfair_key = playfair_key

    def decrypt(self, cipher_text):
        self._cipher_text = cipher_text
        self._decrypt()
        return self._plain_text

    def decrypt_file(self, file):
        self._cipher_text = open(file).read()
        self._decrypt()
        return self._plain_text

    def _decrypt(self):
        self._decrypt_blocks()
        self._construct_plain_text()
        return self._plain_text

    def _construct_plain_text(self):
        self._plain_text = ""
        for block in self._blocks:
            block_text = block.text

            for char in block_text:
                # handle substitute_by and padding_char correctly
                if char == self._playfair_key.substitute_by:
                    self._plain_text += self._playfair_key.substitute_char
                elif char == self._playfair_key.padding_char:
                    continue
                else:
                    self._plain_text += char

        return self._plain_text

    def _decrypt_blocks(self):
        self._blocks = []
        for block in self._iterator():
            # if block only contains special chars, block.ready is false
            if not block.ready:
                # only append the block, since there aren't any chars in it
                self._blocks.append(block)
                continue

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
            rule(self._playfair_key, block, Rule.DECRYPT)
            self._blocks.append(block)

    def _iterator(self):
        block = Block()
        valid_chars = re.compile(r"^[a-z]$")

        for char in self._cipher_text:
            if not valid_chars.match(char):
                block.add_special(char)
                continue

            block.add_char(char)
            if block.ready:
                yield block
                block = Block()

        # if block ends with a single character, add padding char and yield it
        if block.current_char:
            raise ValueError("Invalid cipher_text, couldn't decrypt block!")
        # if block has no chars but has special chars, yield it
        elif block.has_content:
            yield block
