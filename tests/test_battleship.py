#!/usr/bin/env python
# encoding: utf-8
import pytest

from battleship import Ship


def test_battleship_ship_total_positions(ship):
    assert ship.total_positions == len(ship.hit_positions)


def test_battleship_ship_is_destroyed_false(ship, ship_position):
    ship.hit_positions = []

    ship_position['hit'] = False
    ship.hit_positions.append(ship_position)

    ship_position2 = ship_position.copy()
    ship_position2['hit'] = True
    ship.hit_positions.append(ship_position2)
    assert ship.is_destroyed is False
    assert isinstance(ship, Ship)


def test_battleship_ship_is_destroyed_true(ship, ship_position):
    ship.hit_positions = []

    ship_position['hit'] = True
    ship.hit_positions.append(ship_position)

    ship_position2 = ship_position.copy()
    ship_position2['hit'] = True
    ship.hit_positions.append(ship_position2)
    assert ship.is_destroyed is True
    assert isinstance(ship, Ship)


@pytest.mark.parametrize('coordinates,shoot,expected', [
    ((0, 1), (0, 1), True),
    ((10, 15), (0, 1), False),
    ((10, 15), (10, 15), True),
    ((0, 1), (0, 1), True),
])
def test_battleship_ship_hit_with_add_location(ship, coordinates, shoot, expected):
    assert ship.hits == 0
    ship.hit_positions = []
    ship.add_location(coordinates[0], coordinates[1], False)

    ship.hit(shoot[0], shoot[1])
    current = [x['hit'] for x in ship.hit_positions]
    expected_hits = 1 if expected else 0
    assert ship.hits == expected_hits
    assert current[0] == expected
    assert isinstance(ship, Ship)
