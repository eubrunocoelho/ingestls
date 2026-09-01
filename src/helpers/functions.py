import builtins

from flask import current_app

from src.container.di_container import DIContainer
from src.exceptions.dump.debug_exception import DumpException


def debug(value):
    raise DumpException(value)


builtins.debug = debug


def get_container() -> DIContainer:
    return current_app.extensions['container']
