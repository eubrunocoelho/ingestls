from enum import Enum


class PatternKindEnum(str, Enum):
    EXTENSION = 'extension'
    FILE = 'file'
    DIRECTORY = 'directory'
