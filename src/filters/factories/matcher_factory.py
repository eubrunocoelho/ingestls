from src.enums.pattern_kind_enum import PatternKindEnum
from src.filters.matchers.matcher import Matcher

class MatcherFactory:
    def __init__(self):
        self._matchers: dict[PatternKindEnum, Matcher] = {
            PatternKindEnum.EXTENSION: ExtensionMatcher(),
            PatternKindEnum.FILE: FileMatcher(),
            PatternKindEnum.DIRECTORY: DirectoryMatcher(),
        }

    def make(self, kind: PatternKindEnum) -> Matcher:
        try:
            return self._matchers[kind]
        except KeyError:
            raise ValueError(
                f'Matcher não encontrado para \'{kind.value}\'.'
            )