#!/usr/bin/env python
# encoding: utf-8
import os
import gettext


here = os.path.dirname(os.path.abspath(__file__))
locale_dir = os.path.join(here, "locale")


if os.path.exists(locale_dir):
    language = gettext.translation('battleship', localedir=str(locale_dir), languages=['en', 'pt_BR'])
    language.install()
else:
    language = gettext
