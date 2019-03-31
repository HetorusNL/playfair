class CharLocation(object):
    def __init__(self):
        self._row = -1
        self._col = -1

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, new_row):
        if new_row < 0 or new_row > 5:
            raise ValueError("Row must be between 0 and 5!")
        self._row = new_row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, new_col):
        if new_col < 0 or new_col > 5:
            raise ValueError("Col must be between 0 and 5!")
        self._col = new_col

    @property
    def valid(self):
        return self.row != -1 and self.col != -1
