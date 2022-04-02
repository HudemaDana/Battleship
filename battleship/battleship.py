#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime
import random
from copy import deepcopy

from .constants import LETTERS
from .exceptions import InvalidLocation, InvalidCoordinate, InvalidFormat, InvalidShipInitial
from .language import language
_ = language.gettext

MESSAGE_ERROR = _(
    'You need to choose a letter from A to Q \n'
    'and one NUMBER from 0 to 16.'
)


class Ship:

    def __init__(self, name, length, points, initials):
        self.direction = ''
        self.hit_positions = []
        self.initials = initials
        self.length = length
        self.name = name
        self.points = points

    @property
    def hits(self):
        return len([x['hit'] for x in self.hit_positions if x['hit']])

    @property
    def is_destroyed(self):
        results = []
        for position in self.hit_positions:
            results.append(
                position['hit']
            )
        return all(results) if results else False

    @property
    def sunk(self):
        return self.is_destroyed is True

    @property
    def total_positions(self):
        return len(self.hit_positions)

    def add_location(self, x, y, hit):
        if len(self.hit_positions) + 1 > self.length:
            text = 'Ship has more hit positions {} than Lenght: {}'.format(
                len(self.hit_positions) + 1,
                self.length
            )
            raise InvalidLocation(text)

        self.hit_positions.append({
            'x': x,
            'y': y,
            'hit': hit
        })

    def hit(self, x, y):
        for pos in self.hit_positions:
            if (x, y) == (pos['x'], pos['y']):
                pos['hit'] = True

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return "<Ship: {}>".format(self.__str__())


class Board:
    """
    Board Game: Board responsible to create and control all battle area.
    """
    COLS = 17
    ROWS = 17
    SHIP_TYPES = [
        {'name': _('carrier'), 'length': 5, 'points': 250, 'initials': 'CA'},
        {'name': _('battleship'), 'length': 4, 'points': 200, 'initials': 'BT'},
        {'name': _('cruiser'), 'length': 3, 'points': 150, 'initials': 'CR'},
        {'name': _('destroyer'), 'length': 3, 'points': 150, 'initials': 'DT'},
        {'name': _('submarine'), 'length': 2, 'points': 100, 'initials': 'SB'},
        {'name': _('frigate'), 'length': 2, 'points': 100, 'initials': 'FR'},
    ]

    def __init__(self, ships_visible=False):
        self.default_ship_value = {
            'ship': None,
            'shooted': False,
            'visible': ships_visible,
        }
        self.matrix = self.clean_board()
        self.sunken_ships = 0
        self.ships = []
        self.total_hits = 0

    @property
    def total_available_ships(self):
        return len(self.ships)

    @property
    def total_ships(self):
        return len([ship for ship in self.ships if ship.total_positions])

    def _get_ship_from_initials(self, initials):
        for ship_data in self.SHIP_TYPES:
            if ship_data['initials'] == initials:
                return Ship(**ship_data)
        return None

    def add_ship_auto(self, ship):
        direction = random.choice(['v', 'h'])
        ship.direction = direction
        length = ship.length
        x = random.randint(0, self.COLS - length)
        y = random.randint(0, self.ROWS - length)

        try:
            self.validate_new_ship_position(ship.length, x, y, direction)
        except InvalidCoordinate:
            self.remove_ship(ship)
            return self.add_ship_auto(ship)

        board_position = x if direction == 'h' else y
        end_position = (board_position + length)

        for pos in range(board_position, end_position):
            coordinates = x, pos
            if direction == 'v':
                coordinates = pos, y

            ship.add_location(*coordinates, hit=False)
            value = deepcopy(self.default_ship_value)
            value['ship'] = ship
            self.matrix[coordinates[0]][coordinates[1]] = value

        self.ships.append(ship)
        return True

    def add_ship_manualy(self, ship_initials, x, y, direction):
        ship = self._get_ship_from_initials(ship_initials)
        if not ship:
            raise InvalidShipInitial()

        self.validate_new_ship_position(ship.length, x, y, direction)

        ship.direction = direction
        length = ship.length
        board_position = x if direction == 'h' else y
        end_position = (board_position + length)

        for pos in range(board_position, end_position):
            coordinates = x, pos
            if direction == 'v':
                coordinates = pos, y

            ship.add_location(*coordinates, hit=False)
            value = deepcopy(self.default_ship_value)
            value['ship'] = ship
            self.matrix[coordinates[0]][coordinates[1]] = value

        self.ships.append(ship)
        return True

    def validate_new_ship_position(self, ship_length, x, y, direction):
        board_position = x if direction == 'h' else y
        end_of_board = self.COLS if direction == 'h' else self.ROWS
        end_position = (board_position + ship_length)

        if end_position > end_of_board:
            msg = 'Invalid Coordinate: The boat was off the board.'
            raise InvalidCoordinate(msg)

        for pos in range(board_position, end_position):
            coordinates = x, pos
            if direction == 'v':
                coordinates = pos, y

            if not self.is_available(*coordinates):
                msg = 'Invalid Coordinate: Already exists a boat in this coordinate.'
                raise InvalidCoordinate(msg)
        return True

    def auto_build_fleet(self):
        for ship_type in self.SHIP_TYPES:
            ship = Ship(**ship_type)
            self.add_ship_auto(ship)

    def clean_board(self):
        default_ship_value = deepcopy(self.default_ship_value)
        return [[default_ship_value for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def is_available(self, x, y):
        return self.matrix[x][y] == deepcopy(self.default_ship_value)

    def is_finished(self):
        results = []
        for ship in self.ships:
            results.append(
                ship.is_destroyed
            )
        return all(results)

    def remove_ship(self, ship):
        for position in ship.hit_positions:
            self.matrix[position['x']][position['y']] = deepcopy(self.default_ship_value)

    def shot(self, x, y):
        position = self.matrix[x][y].copy()

        if position['shooted']:
            return False, None

        position.update(shooted=True)
        if not position['ship']:
            self.matrix[x][y] = position
            return False, None

        position['ship'].hit(x, y)

        self.total_hits += 1
        if position['ship'].is_destroyed:
            self.sunken_ships += 1

        self.matrix[x][y] = position
        return True, position['ship']


class Game(Board):

    def __init__(self, player, ships_visible=False):
        super().__init__(ships_visible=ships_visible)
        self.player = player
        self.start_time = datetime.now()
        self.shots = 0
        self.points = 0
        self.lost_shot = 0
        self.right_shot = 0

    @property
    def time_elapsed(self):
        end_time = datetime.now()
        return (end_time - self.start_time).total_seconds()

    def clean_board(self):
        default_ship_value = deepcopy(self.default_ship_value)
        return [[default_ship_value for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def _get_coordinates_from_raw(self, raw_x, raw_y):
        try:
            x = int(LETTERS[raw_x.lower()])
            y = int(raw_y.strip())
        except ValueError:
            msg = _('Invalid Format. {}. Coordinate: {}{}').format(MESSAGE_ERROR, raw_x, raw_y)
            raise InvalidFormat(msg)

        if x not in range(self.COLS) or y not in range(self.ROWS):
            msg = _('Invalid Coordinate. {}. Coordinate: {}{}').format(MESSAGE_ERROR, raw_x, raw_y)
            raise InvalidCoordinate(msg)
        return x, y

    def play(self, raw_x, raw_y):
        x, y = self._get_coordinates_from_raw(raw_x, raw_y)

        if self.matrix[x][y]['shooted']:
            msg = _('Invalid Coodinate. Already Used.').format(MESSAGE_ERROR, raw_x, raw_y)
            raise InvalidCoordinate(msg)
        else:
            self.shots += 1

            hit, ship = self.shot(x, y)

            if not hit:
                self.lost_shot += 1
                return False, None

            self.right_shot += 1
            self.points += ship.points
            return True, ship

    def __str__(self):
        return self.player.title()

    def __repr__(self):
        return "<Game: Player: {}>".format(self.__str__())
