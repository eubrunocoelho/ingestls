from enum import Enum


class PatternTypeEnum(str, Enum):
    INCLUDE = 'include'
    EXCLUDE = 'exclude'
