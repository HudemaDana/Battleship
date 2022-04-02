#!/usr/bin/env python
# encoding: utf-8

from battleship.main import main


def test_main_general(cli_runner):
    result = cli_runner.invoke(main)
    assert 'Usage: main' in result.output
