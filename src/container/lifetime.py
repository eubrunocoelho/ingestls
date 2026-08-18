from enum import Enum


class Lifetime(str, Enum):
    TRANSIENT = 'transient'
    SINGLETON = 'singleton'
