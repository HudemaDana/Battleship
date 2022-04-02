#!/usr/bin/env python
# encoding: utf-8
import click

from click import echo as cprint, style as st

from .constants import NUMBERS
from .language import language
_ = language.gettext

table_length = 90
dash = '-' * table_length

SHIP_COLORS = {
    'CA': 'green',
    'BT': 'bright_white',
    'CR': 'bright_yellow',
    'DT': 'magenta',
    'SB': 'cyan',
    'FR': 'blue'
}


def print_statistics(game_board1, game_board2):
    print('Player1: {:<86}'.format(game_board1.player.title()), end='')
    print('Player2: {:<20}'.format(game_board2.player.title() if game_board2.player != 'CPU' else game_board2.player))

    print(dash, end='')
    print('{:^5}'.format(''), end='')
    print(dash)
    print(_('Points: '), game_board1.points, end="     ")
    print(_('Shots: '), game_board1.shots, end="     ")
    print(_('Time elapsed: '), '{} sec'.format(int(game_board1.time_elapsed)), end="")

    print('{:^43}'.format(''), end='')
    print(_('Points: '), game_board2.points, end="     ")
    print(_('Shots: '), game_board2.shots, end="     ")
    print(_('Time elapsed: '), '{} sec'.format(int(game_board2.time_elapsed)), end="\n")
    print('{}{:^5}{}'.format(dash, '', dash))


def get_col_value(col):
    if col['shooted']:
        if not col['ship']:
            return st('{:^4}'.format('O'), fg='yellow')
        else:
            return st('{:^4}'.format(col['ship'].initials), fg='red')
    else:
        if col['visible'] and col['ship']:
            color = SHIP_COLORS[col['ship'].initials]
            return st('{:^4}'.format(col['ship'].initials), fg=color)
        return st('{:^4}'.format('.'), fg='white')


def print_board(game_board1, game_board2):
    click.clear()
    print_statistics(game_board1, game_board2)

    # Table Header
    cprint('|{:^3}|'.format('-'), nl=False)
    for i in range(game_board1.COLS):
        cprint('{:^4}|'.format(i), nl=False)

    cprint('{:^5}|'.format(''), nl=False)
    cprint('{:^3}|'.format('-'), nl=False)
    for i in range(game_board1.COLS):
        cprint('{:^4}|'.format(i), nl=False)

    cprint()
    cprint('{}{:^5}{}'.format(dash, '', dash))

    # Table Body
    for i, (board1_row, board2_row) in enumerate(zip(game_board1.matrix, game_board2.matrix)):
        cprint('|', nl=False)
        cprint('{:^3}'.format(NUMBERS[i].upper()), nl=False)
        cprint('|', nl=False)

        for col in board1_row:
            cprint(get_col_value(col), nl=False)
            cprint('|', nl=False)

        cprint('{:^5}'.format(''), nl=False)
        cprint('|{:^3}|'.format(NUMBERS[i].upper()), nl=False)
        for col2 in board2_row:
            cprint(get_col_value(col2), nl=False)
            cprint('|', nl=False)

        cprint()

    cprint('{}{:^5}{}'.format(dash, '', dash))
    cprint()

    # Labels
    cprint(_('Labels'))
    for i, (board_ship, board2_ship) in enumerate(zip(game_board1.ships, game_board2.ships)):
        ship_color = SHIP_COLORS[board_ship.initials]
        ship_color2 = SHIP_COLORS[board2_ship.initials]

        data_board_ship = (
            _(board_ship.name.title()),
            st('{:^11}'.format(board_ship.initials), fg=ship_color),
            board_ship.length,
            board_ship.hits,
            _('yes') if board_ship.sunk else _('no')
        )
        data_board2_ship = (
            _(board2_ship.name.title()),
            st('{:^11}'.format(board2_ship.initials), fg=ship_color2),
            board2_ship.length,
            board2_ship.hits,
            _('yes') if board2_ship.sunk else _('no')
        )
        if i == 0:
            cprint(dash, nl=False)
            cprint('{:^5}'.format(''), nl=False)
            cprint(dash)
            label_header = (_('Ship'), _('Initials'), _('Size'), _('Hits'), _('sunk'))
            cprint('{:<13}{:^11}{:^8}{:^8}{:^10}'.format(*label_header), nl=False)
            cprint('{:^45}'.format(''), nl=False)
            cprint('{:<13}{:^11}{:^8}{:^8}{:^10}'.format(*label_header))
            cprint(dash, nl=False)
            cprint('{:^5}'.format(''), nl=False)
            cprint(dash)
            cprint('{:<13}{}{:^8}{:^8}{:^10}'.format(*data_board_ship), nl=False)
            cprint('{:^45}'.format(''), nl=False)
            cprint('{:<13}{}{:^8}{:^8}{:^10}'.format(*data_board2_ship))
        else:
            cprint('{:<13}{}{:^8}{:^8}{:^10}'.format(*data_board_ship), nl=False)
            cprint('{:^45}'.format(''), nl=False)
            cprint('{:<13}{}{:^8}{:^8}{:^10}'.format(*data_board2_ship))

    cprint()
    cprint(dash, nl=False)
    cprint('{:^5}'.format(''), nl=False)
    cprint(dash)


def print_ship_hit(ship_hit, player):
    click.clear()
    cprint('\n\n\n\n')

    if ship_hit.sunk:
        if player == 1:
            message = _('You Destroy a {}.').format(ship_hit.name.title())
        else:
            message = _('Your {} was Destroyed.').format(ship_hit.name.title())
    else:
        if player == 1:
            message = _('You Hit a {}.').format(ship_hit.name.title())
        else:
            message = _('Your {} was Hit.').format(ship_hit.name.title())

    cprint(st('{:^88}'.format(message), fg='green'))

    cprint('\n\n\n\n')
    input(_("Press Enter to continue..."))


def print_error_message(message):
    click.clear()
    cprint(dash)
    cprint('\n\n\n\n')

    cprint(st('{:^88}'.format(message), fg='red'))

    cprint('\n\n\n\n')
    cprint(dash)
    input(_("Press Enter to continue..."))


def print_status(game_board, win=False):
    click.clear()
    print(_('\nPoints: '), game_board.points, end="     ")
    print(_('Lost Shots: '), game_board.lost_shot, end="     ")
    print(_('Right Shots: '), game_board.right_shot, end="     ")
    cprint(dash)

    if win:
        message = st('\n\n\n{:^90}'.format(_('You WIN !!!!!')), fg='green')
    else:
        message = st('\n\n\n{:^90}'.format(_('You Lost !!!!!')), fg='red')

    cprint(message)
    cprint('\n\n\n')
    cprint(dash)
    print(_('Sunken Ships: '), game_board.sunken_ships, end="     ")
    print(_('Missing Ships: '), game_board.total_ships - game_board.sunken_ships, end="   ")
    print(_('Time elapsed: {} sec').format(int(game_board.time_elapsed)), end="\n")

    for i, ship in enumerate(game_board.ships):
        data_board_ship = (
            _(ship.name.title()),
            ship.hits,
            _('yes') if ship.sunk else _('no')
        )
        if i == 0:
            cprint(dash)
            label_header = (_('Ship'), _('Hits'), _('sunk'))
            cprint('{:<13}{:^8}{:^10}'.format(*label_header))
            cprint(dash)
            cprint('{:<13}{:^8}{:^10}'.format(*data_board_ship))
        else:
            cprint('{:<13}{:^8}{:^10}'.format(*data_board_ship))

    cprint(dash)
