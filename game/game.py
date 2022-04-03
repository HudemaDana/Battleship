from exceptions.exceptions import BoardException
from valid.valid_place_board import ValidPlace


class Game:
    def __init__(self, board_player, computer):
        self.player = board_player
        self.computer = computer

    def meniu_frumix(self):
        print("\n\n    -*-*-*- BATTLESHIP -*-*-*-\n\n")
        smth = input(" ~ PRESS ENTER TO START THE GAME ~")

    def menu_computer(self):
        print("\nCOMPUTER HAS CREATED ITS BOARD")
        print("IT'S TIME TO MAKE THE ENEMY SUFFER A TERRIBLE LOSE! ARE YOU READY?!")
        print("\t\t 1. YES!!! LET'S GOOOOO")
        print("\t\t 2. NO....")
        decision = str(input("DECISION = "))
        if decision == '1':
            print("Ok, then make your first move")
        elif decision == '2':
            print("It's not democracy here, don't be a chicken")

    def choose_part1_of_the_game(self):
        i = 0
        while i < 5:
            nr = 0
            for j in self.player.get_ship_board:
                if nr != 0:
                    print(" | ".join(j))
                else:
                    print("   ".join(j))
                nr = nr + 1

            ship = str(input("\n\nYOUR SHIP CAN BE B,C,D,P or S : "))
            row = str(input("ROW FROM A TO J : "))
            column = str(input("COLUMN FROM 1 TO 10 : "))
            orientation = str(input("VERTICAL (V) / HORIZONTALLY (O) : "))
            print("\n")

            ok = 0
            try:
                self.player.put_ship(ship, row, column, orientation)
                ok = 1
            except BoardException as be:
                print(be)

            if ok == 1:
                i = i + 1

    def try_to_hit_enemy_ship(self, row, column):
        """

        :param row:
        :param column:
        :return: well, it's trying to hit the enemy
        """
        ship = 0
        valid = ValidPlace(str(row), str(column))
        if valid.valid_place():
            row = row.upper()
            row = ord(row) - 64
            column = int(column)
            is_ship = False
            if self.computer.board_computer.get_ship_board[row][column] != 'O':
                is_ship = True
                '''
                if the player hits a part of a ship, computer take the name of the ship and contor it so when the hits 
                are equal with the len means the ship is sunk
                
                just the computer can know if he is losing or not
                '''
                ship = self.computer.board_computer.get_ship_board[row][column]
                self.computer.board_computer.available_ships[ship][2] = \
                    self.computer.board_computer.available_ships[ship][2] + 1

                '''
                i have to put this part of code in controller
                '''
                if self.computer.sunk_ship(ship) == True:
                    print("\n--------------------------")
                    print("SHIP " + str(ship) + " IS SUNK")
                    print("\n--------------------------")
                # if self.computer.computer_lost() == True:
                #     print(" YOU WON!!!!!!!!!!!!!!!!!!\n CONGRATS! \n GO AND TAKE A SHOT, YOU DESERVE IT <3")
                #     return
                # if self.computer.sunk_ship(ship) == True:
                #     print("SHIP"+ str(ship)+ "IS SUNK")

            self.player.add_on_check_board(row, column, is_ship)

            print("\n")
            nr = 0
            for j in self.player.get_check_board:
                if nr != 0:
                    print(" | ".join(j))
                else:
                    print("   ".join(j))
                nr = nr + 1
        else:
            print("wrong input")
            return 0
        return 1

    def sunk_ship(self, ship):
        """

        :param ship:
        :return: verify if the given ship is dead
        """
        if self.player.available_ships[ship][2] == self.player.available_ships[ship][0]:
            return True
        return False

    def player_lost(self):
        """

        :return: verify if the player lost
        """
        for key in self.player.available_ships:
            if self.sunk_ship(str(key)) == False:
                return False
        return True

    def place_ships_on_the_map(self):
        self.choose_part1_of_the_game()
        self.computer.choose_part1_of_the_game()

    def controller(self):
        self.meniu_frumix()

        name = str(input("CHOOSE YOUR USERNAME: "))
        self.place_ships_on_the_map()
        self.menu_computer()

        '''
        turn shows who's turn is to move on the table
        if  turn --> 0 (player)
            turn --> 1 (computer)
        '''
        turn = 0
        while True:
            if turn == 0:
                row = str(input("\nROW FROM A TO J : "))
                column = str(input("COLUMN FROM 1 TO 10 : "))
                turn = self.try_to_hit_enemy_ship(row, column)
                if self.computer.computer_lost() == True:
                    print("\tYOU WON!!!!!!!!!!!!!!!!!!\n CONGRATS! \n GO AND TAKE A SHOT, YOU DESERVE IT <3")
                    return
            else:
                is_ship = self.computer.hit_player_ship()
                if is_ship == True:
                    print("\n--------------------------")
                    print("\tCOMPUTER HIT A PART OF YOUR SHIP")
                    print("--------------------------")
                else:
                    print("\n--------------------------")
                    print("\tCOMPUTER HIT WATER")
                    print("--------------------------")

                nr = 0
                print("\n")
                for j in self.computer.board_computer.get_check_board:
                    if nr != 0:
                        print(" | ".join(j))
                    else:
                        print("   ".join(j))
                    nr = nr + 1

                if self.player_lost() == True:
                    print(" COMPUTER WON.... MAYBE NEXT TIME HOMIE.... GO PLAY SOME LOL....")
                    return
                turn = 0
