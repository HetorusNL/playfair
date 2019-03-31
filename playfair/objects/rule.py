class Rule(object):
    @classmethod
    def row(cls, playfair_key, block):
        for i in range(2):
            cl = playfair_key.char_location(block.char(i))

            # increment index with roll over
            index = cl.col + 1 if cl.col < 4 else 0
            new_char = playfair_key._tableau_row[cl.row][index]

            # replace the char in the block with new_char
            block.replace_char(i, new_char)

    @classmethod
    def col(cls, playfair_key, block):
        for i in range(2):
            cl = playfair_key.char_location(block.char(i))

            # increment index with roll over
            index = cl.row + 1 if cl.row < 4 else 0
            new_char = playfair_key._tableau_col[cl.col][index]

            # replace the char in the block with the new_char
            block.replace_char(i, new_char)

    @classmethod
    def rect(cls, playfair_key, block):
        # get the char locations of both characters in the block
        cl0 = playfair_key.char_location(block.char(0))
        cl1 = playfair_key.char_location(block.char(1))

        # switch the column locations of both characters around
        new_char_0 = playfair_key._tableau_row[cl0.row][cl1.col]
        new_char_1 = playfair_key._tableau_row[cl1.row][cl0.col]

        # replace the characters in the block
        block.replace_char(0, new_char_0)
        block.replace_char(1, new_char_1)
