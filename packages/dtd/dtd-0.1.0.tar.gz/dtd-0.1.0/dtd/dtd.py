"""Main module."""

import pathlib

from . import DS_STORE_FILENAME


def iterdir(*args, **kwargs):
    return filter(lambda x: x.name != DS_STORE_FILENAME, iterdir.original(*args, **kwargs))


iterdir.original = pathlib.Path.iterdir


def patch_all():
    pathlib.Path.iterdir = iterdir
