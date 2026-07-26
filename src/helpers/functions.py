from pprint import pprint
import sys
import builtins


def dd(value):
    pprint(value)
    sys.exit()


builtins.dd = dd
