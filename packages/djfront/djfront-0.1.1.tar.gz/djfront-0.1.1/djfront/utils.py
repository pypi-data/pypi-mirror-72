#!/usr/bin/env python3
#                            _                _____
#      /\                   | |       /\     |_   _|
#     /  \     ____   __ _  | |_     /  \      | |
#    / /\ \   |_  /  / _` | | __|   / /\ \     | |
#   / ____ \   / /  | (_| | | |_   / ____ \   _| |_
#  /_/    \_\ /___|  \__,_|  \__| /_/    \_\ |_____|
#
#
import os
from glob import glob
from pathlib import Path

here = os.getcwd()


def get_all_htmls():
    """
    Get all html files in current directory, return None if none of html files found.
    :return: list
    """
    pattern = f"{here}/*.html"
    htmls = glob(pattern)
    return htmls


def prepare_dirs():
    """
    check whether some dirs already created, if not create a new one.called
    djstatic and djtemplates.
    :return:
    """
    for each in ['static', 'templates']:
        if os.path.isdir(os.path.join(here, each)):
            pass
        else:
            os.mkdir(os.path.join(here, each))
