#!/usr/bin/env python
# encoding: utf-8
import random

import pytest
from click.testing import CliRunner

from battleship import Ship


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def ship_data():
    return {
        'name': 'battleship',
        'length': 4,
        'points': 200,
        'initials': 'BT'
    }


@pytest.fixture
def ship_position():
    return {
        'x': random.randint(0, 16),
        'y': random.randint(0, 16),
        'hit': False
    }


@pytest.fixture
def ship(ship_data):
    ship = Ship(**ship_data)
    for _ in range(4):
        ship.hit_positions.append({
            'x': random.randint(0, 16),
            'y': random.randint(0, 16),
            'hit': False
        })
    return ship
