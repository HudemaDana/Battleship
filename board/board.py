from exceptions.exceptions import BoardException
from valid.valid_place_board import ValidPlace


class Board:
    def __init__(self):
        self.ship_board = []
        self.check_board = []
        self.available_ships = {"C": [5, 1, 0], "B": [4, 1, 0], "D": [3, 1, 0], "S": [3, 1, 0], "P": [2, 1, 0]}
        self.create_boards()

    def create_boards(self):
        """
        :return: it creates 2 boards:
        --> first : board to put your own ships, where:
                    --> O - water
                    --> B,C,D,P,S - ships
        --> second: board with your moves on the opponent board,where:
                    --> O - unknown spaces
                    --> W - water
                    --> * - hit ship

        """
        self.ship_board = [['O' for i in range(11)] for i in range(11)]
        self.check_board = [['O' for i in range(11)] for i in range(11)]

        alphabet = 'ABCDEFGHIJ'
        for i in range(len(alphabet)):
            self.ship_board[i + 1][0] = alphabet[i]

        for i in range(10):
            self.ship_board[0][i + 1] = str(i + 1)

        for i in range(len(alphabet)):
            self.check_board[i + 1][0] = alphabet[i]

        for i in range(10):
            self.check_board[0][i + 1] = str(i + 1)

        # for i in self.check_board:
        #    print(" ".join(i))

    @property
    def get_ship_board(self):
        return self.ship_board

    @property
    def get_check_board(self):
        return self.check_board

    # for adding on the ship_board list

    def valid_ship(self, ship):
        ship = ship.upper()
        if ship in self.available_ships and self.available_ships[ship][1] != 0:
            return True
        return False

    def valid_orientation(self, ship, row, column, orientation):
        """

        :param ship:
        :param row:
        :param column:
        :param orientation:
        :return: verify is i can place the boat with the given orientation
        """
        if orientation == 'V':
            if row + ship - 1 > 10:
                return False
            else:
                for i in range(row, row + ship):
                    if self.ship_board[i][column] != 'O':
                        return False
                return True

        elif orientation == 'O':
            if column + ship - 1 > 10:
                return False
            else:
                for i in range(column, column + ship):
                    if self.ship_board[row][i] != 'O':
                        return False
                return True
        else:
            return False

    def put_ship(self, ship, row, column, orientation):

        """

        :param ship:
        :param row:
        :param column:
        :param orientation:
        :return: verifiy if I can place the boat somewhere and then gg I put  it there
        """
        valid = ValidPlace(str(row), str(column))
        if self.valid_ship(ship) and valid.valid_place():
            ship = ship.upper()
            row = row.upper()
            row = ord(row) - 64
            column = int(column)
            if self.valid_orientation(self.available_ships[ship][0], row, column, orientation):
                if orientation == 'V':
                    for i in range(row, row + self.available_ships[ship][0]):
                        self.ship_board[i][column] = ship
                else:
                    for i in range(column, column + self.available_ships[ship][0]):
                        self.ship_board[row][i] = ship
                self.available_ships[ship][1] = 0
            else:
                raise BoardException("Wrong input for orientation")
        else:
            raise BoardException("Wrong input for ship/place")

    def add_on_check_board(self, row, column, is_ship):
        """
        :return: * --> hit ship
                 W --> water
        """
        if is_ship == True:
            self.check_board[row][column] = '*'
        else:
            self.check_board[row][column] = 'W'
