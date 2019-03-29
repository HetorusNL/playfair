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
