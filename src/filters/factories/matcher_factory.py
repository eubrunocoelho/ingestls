from src.filters.matchers.directory_matcher import DirectoryMatcher
from src.filters.matchers.extension_matcher import ExtensionMatcher
from src.filters.matchers.file_matcher import FileMatcher
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
        matcher = self._matchers.get(kind)

        if matcher is None:
            raise ValueError(
                f'Matcher não encontrado para \'{kind.value}\'.'
            )

        return matcher
