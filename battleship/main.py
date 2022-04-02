#!/usr/bin/env python
# encoding: utf-8
import sys
import time

import click
from click import style as st
from click.exceptions import Abort as AbortException

from .battleship import Game
from .exceptions import InvalidCoordinate, InvalidFormat
from .language import language
from .robot import Brainiac
from .version import __version__

from . import printer
_ = language.gettext


def player_shot(board_opponent, player, robot=None):
    if robot:
        x, y = robot.shot()
    else:
        result = click.prompt(_(
            'Choose your coordinate using one LETTER from A to Q and one NUMBER from 0 to '
            '16. \n'
            'Ex: a1, b15, c10 and etc... \n\nCoordinate: '
        ))
        x, y = result[0], result[1:]

    try:
        hit, ship = board_opponent.play(str(x), str(y))
    except (InvalidFormat, InvalidCoordinate) as exc:
        click.clear()
        printer.print_error_message(_(str(exc)))
        return False

    # passing the shot status to Robot learn
    if robot:
        robot.shot_status(x, y, ship)

    if hit:
        printer.print_ship_hit(ship, player)
        return True

    # Check if Wins
    if board_opponent.is_finished():
        sys.exit(printer.print_status(board_opponent, win=True))

    return True


@click.group()
@click.version_option(version=__version__, message='Py-Battleship, version %(version)s')
def main():
    """Py-Battleship.

    Is a simple Battleship game in text mode. Lets play!

    \b
    Example:
    \b
    \t $ py-battleship play
    """


@main.command('play')
def play():
    """Start Game
    """
    click.clear()
    player1_name = click.prompt(_('Player1  name: '))

    click.clear()
    players = click.prompt(_('Choose one or two players: '), type=click.Choice(['1', '2']))

    player2_name = 'CPU'
    if players == 2:
        player2_name = click.prompt(_('Player1  name: '))

    click.clear()
    player1_auto_build = click.prompt(_(
        'Do you want place your ships your self or \n'
        'you prefer to let automatic.\n\n'
        '1- Automatic \n'
        '0 - Place Own \n'
        'Choose: '), type=click.Choice(['0', '1'])
    )

    game_board1 = Game(
        player=player1_name,
        ships_visible=True
    )

    if bool(player1_auto_build):
        game_board1.auto_build_fleet()

    player2_autobuild = '1'
    if players == 2:
        player2_autobuild = click.prompt(_(
            'Do you want place your ships your self or \n'
            'you prefer to let automatic.\n\n'
            '1 - Automatic \n'
            '0 - Place Own \n'
            'Choose: '), type=click.Choice(['0', '1'])
        )

    game_board2 = Game(
        player=player2_name,
        ships_visible=False
    )
    if bool(player2_autobuild):
        game_board2.auto_build_fleet()

    try:
        while True:
            while True:
                printer.print_board(game_board1, game_board2)
                click.echo(st(_('Press CTRL+C to exit ...')))

                # Player1 Move against Player2
                if not player_shot(board_opponent=game_board2, player=1):
                    break

                # Check if Player1 Wins
                if game_board2.is_finished:
                    printer.print_status(game_board2, win=True)

                printer.print_board(game_board1, game_board2)

                # Player 2 shot
                robot = None
                if game_board2.player == 'CPU':
                    robot = Brainiac(game_board2)
                    click.echo('Player 2 is choosing a coordinate.')
                    time.sleep(2)

                # Player2 Move against Player1
                if not player_shot(board_opponent=game_board1, player=2, robot=robot):
                    break

                # Check if Player2 Wins
                if game_board1.is_finished:
                    printer.print_status(game_board1, win=False)

            printer.print_board(game_board1, game_board2)

    except (KeyboardInterrupt, AbortException):
        # TODO: Show statistics of the two player, for now is showing only for player1
        sys.exit(printer.print_status(game_board2))
