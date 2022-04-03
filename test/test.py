import unittest
from board.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board_player = Board()

    def tearDown(self) -> None:
        pass

    def test_board_print(self):
        self.board_player.create_boards()
        self.assertEqual(len(self.board_player.ship_board), 11)

    def test_create_ships(self):
        self.assertEqual(self.board_player.available_ships,
                         {"C": [5, 1], "B": [4, 1], "D": [3, 1], "S": [3, 1], "P": [2, 1]})

