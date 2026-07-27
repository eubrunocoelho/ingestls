import re

from src.enums.pattern_kind_enum import PatternKindEnum
from src.validators.pattern_rules.pattern_rule import PatternRule


class DirectoryPatternRule(PatternRule):
    _regex = re.compile(r'^[A-Za-z0-9._-]+/$')

    def match(self, pattern: str) -> PatternKindEnum | None:
        if self._regex.fullmatch(pattern):
            return PatternKindEnum.DIRECTORY

        return None
