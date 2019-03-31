class Char(object):
    def __init__(self, index, char):
        # validate the types of the input arguments
        if type(index) != int:
            raise ValueError("Index must be of type int!")
        if type(char) != str:
            raise ValueError("Char must be of type str!")

        # store the arguments
        self._index = index
        self._char = char

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        if type(new_index) != int:
            raise ValueError("Index must be of type int!")
        self._index = new_index

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, new_char):
        if type(new_char) != str:
            raise ValueError("Char must be of type str!")
        self._char = new_char
