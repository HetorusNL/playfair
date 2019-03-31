from .char import Char


class Block(object):
    def __init__(self):
        self._chars = []
        self._specials = []
        self._index = 0

    def add_char(self, char):
        if len(self._chars) > 1:
            chars = [c.char for c in self._chars]
            raise ValueError("More than 1 char available! ({})".format(chars))

        self._chars.append(Char(self._index, char))
        self._index += 1

    def add_special(self, char):
        self._specials.append(Char(self._index, char))
        self._index += 1

    @property
    def current_char(self):
        if len(self._chars) == 1:
            return self._chars[0].char

        return None

    @property
    def ready(self):
        return len(self._chars) == 2

    @property
    def has_content(self):
        return self._index != 0

    def char(self, location):
        if not self.ready:
            raise ValueError("Block is not yet ready!")

        if location < 0 or location > 1:
            raise ValueError("Only locations [0-1] can be requested!")

        return self._chars[location].char

    def replace_char(self, location, char):
        if not self.ready:
            raise ValueError("Block is not yet ready!")

        if location < 0 or location > 1:
            raise ValueError("Only locations [0-1] can be replaced!")

        self._chars[location].char = char

    @property
    def text(self):
        # the text that is returned (plaintext or ciphertext)
        text = ""
        # the current index of both arrays, chars and specials
        cindex = 0
        sindex = 0
        # length of both arrays, chars and specials
        lc = len(self._chars)
        ls = len(self._specials)
        # the next char in the arrays, if available
        next_char = self._chars[cindex] if lc > cindex else None
        next_special = self._specials[sindex] if ls > sindex else None
        # increment index if statements above are True
        cindex = cindex + 1 if next_char else cindex
        sindex = sindex + 1 if next_special else sindex

        for i in range(self._index):
            if next_char and next_char.index == i:
                # append if next_char and next_char has the correct index
                text += next_char.char
                # get next next_char if available
                next_char = self._chars[cindex] if lc > cindex else None
                # increment cindex if above is True
                cindex = cindex + 1 if next_char else cindex

            elif next_special and next_special.index == i:
                # append if next_special and next_special has the correct index
                text += next_special.char
                # get next next_special if available
                next_special = self._specials[sindex] if ls > sindex else None
                # increment sindex if above is True
                sindex = sindex + 1 if next_special else sindex

            else:
                raise ValueError("No char or special with index {}!".format(i))

        return text
