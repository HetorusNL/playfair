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

    @property
    def char(self):
        return self._char
