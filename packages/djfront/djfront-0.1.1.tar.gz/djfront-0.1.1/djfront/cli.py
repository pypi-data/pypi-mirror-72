#!/usr/bin/env python3
#                            _                _____
#      /\                   | |       /\     |_   _|
#     /  \     ____   __ _  | |_     /  \      | |
#    / /\ \   |_  /  / _` | | __|   / /\ \     | |
#   / ____ \   / /  | (_| | | |_   / ____ \   _| |_
#  /_/    \_\ /___|  \__,_|  \__| /_/    \_\ |_____|
#
#

"""
0. get all the html file lists from the current directory.

htmls = []

1. check whether destination is a django app dir.
HOW ?
django app dir always has a manage.py file. that is always works as a django app dir.

2. find the index.html file at first and get the html file resources.
"""
from .utils import prepare_dirs
import click


def cli():
    click.secho('Thanks for Using AzatAI Django Frontend tool!', fg='blue')
    click.secho('Checking for static and templates directories...')
    prepare_dirs()