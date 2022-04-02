import random

from .battleship import Game
from .constants import LETTERS


class Brainiac:
    """Decision Robot
    TODO: Change when hit a Ship
    """
    shot_directions = ('l', 'r', 'd', 'u')

    def __init__(self, player_board):
        self.player_board = player_board
        self.matrix = self._clean_board()
        self.selected = []
        self.shoots = []
        self.last_shot_direction = ''
        self.current_direction = 'l'

    def _clean_board(self):
        return [[None for _ in range(Game.COLS)] for _ in range(Game.ROWS)]

    def _next_search_direction(self):
        direction = self.shot_directions
        self.current_direction = direction[direction.index(self.current_direction) + 1]

    def _ship_hits(self, ship):
        hits = []
        for i_row, row in enumerate(self.matrix):
            for i_col, col in enumerate(row):
                hits.append((i_row, i_col)) if col == ship else None
        return hits

    def _get_random_shot(self):
        x = random.choice(list(LETTERS.keys())[:17])
        y = random.randint(0, Game.ROWS - 1)
        if (x, y) in self.selected:
            self._get_random_shot()

        self.selected.append((x, y))
        return x, y

    def _get_near_shot(self):
        *coordinates, ship = self.get_last_shot().values()

        if not ship:
            *coordinates, ship = self.get_before_last_shot().values()
            self._next_search_direction()

        x, y = coordinates
        if self.current_direction == 'l':
            coordinates = x + 1, y
        elif self.current_direction == 'r':
            coordinates = x - 1, y
        elif self.current_direction == 'd':
            coordinates = x, y + 1
        elif self.current_direction == 'u':
            coordinates = x, y - 1

        return coordinates

    def get_last_shot(self):
        return self.shoots[-1] if len(self.shoots) else {}

    def get_before_last_shot(self):
        return self.shoots[-2] if len(self.shoots) > 1 else {}

    def shot(self):
        last_shot = self.get_last_shot()
        before_last_shot = self.get_before_last_shot()
        if not last_shot.get('ship', '') and not before_last_shot.get('ship', ''):
            return self._get_random_shot()

        return self._get_near_shot()

    def shot_status(self, raw_x, raw_y, ship):
        x = int(LETTERS[raw_x.lower()])
        y = int(raw_y)

        self.shoots.append({
            'x': x,
            'y': y,
            'ship': ship
        })
        self.matrix[x][y] = ship
