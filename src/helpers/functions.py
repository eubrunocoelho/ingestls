import builtins

from src.exceptions.dump.debug_exception import DumpException


def debug(value):
    raise DumpException(value)

builtins.debug = debug