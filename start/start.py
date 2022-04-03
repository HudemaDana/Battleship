from board.board import Board
from computer.computer import Computer
from game.game import Game
from valid.valid_place_board import ValidPlace


def main():
    board_player = Board()
    board_computer = Board()
    computer = Computer(board_computer, board_player)
    game = Game(board_player, computer)

    game.controller()


main()
