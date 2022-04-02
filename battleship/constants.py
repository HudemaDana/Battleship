#!/usr/bin/env python
# encoding: utf-8
from string import ascii_lowercase


LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=0)}
NUMBERS = {index: letter for index, letter in enumerate(ascii_lowercase, start=0)}
