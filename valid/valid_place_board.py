class ValidPlace:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def valid_place(self):

        if self.column.isdigit() == False or self.row.isalpha() == False:
            return False
        if len(self.row) > 1 or int(self.column) > 10 or int(self.column) < 1:
            return False
        letter = ord(self.row.upper()) - 64
        number = int(self.column)

        if letter > 10 or number > 10 or number == 0 or letter == 0:
            return False

        return True
