import random
from exceptions.exceptions import BoardException


class Computer:
    def __init__(self, board_computer, player_board):
        self.board_computer = board_computer
        self.player_board = player_board

    def choose_part1_of_the_game(self):
        i = 0
        while i < 5:
            ship = random.choice(['C', 'B', 'D', 'S', 'P'])
            row = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
            column = random.randint(1, 10)
            orientation = random.choice(['V', 'O'])
            try:
                self.board_computer.put_ship(ship, row, column, orientation)
            except BoardException:
                i = i - 1
            i = i + 1

    def hit_player_ship(self):
        row = random.randint(1, 10)
        column = random.randint(1, 10)
        while self.board_computer.get_check_board[row][column] != 'O':
            row = random.randint(1, 10)
            column = random.randint(1, 10)

        is_ship = False
        if self.player_board.get_ship_board[row][column] != 'O':
            is_ship = True
            '''
            if the computer hits a part of a ship, the name of the ship will be saved and increased a contor which is gonna 
            play a role in deciding if the ship is sunk(if the contor if equal with the len of the ship)
            
            just the player can know if he's losing or not
            '''
            ship = self.player_board.get_ship_board[row][column]
            self.player_board.available_ships[ship][2] = \
                self.player_board.available_ships[ship][2] + 1


        self.board_computer.add_on_check_board(row, column, is_ship)
        return is_ship


    def sunk_ship(self, ship):
        if self.board_computer.available_ships[ship][2] == self.board_computer.available_ships[ship][0]:
            return True
        return False

    def computer_lost(self):
        for key in self.board_computer.available_ships:
            if self.sunk_ship(str(key)) == False:
                return False
        return True
