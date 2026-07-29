from enum import Enum


class PatternScopeEnum(str, Enum):
    GLOBAL = 'global'
    RECURSIVE = 'recursive'
    PATH = 'path'
