import re

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.pattern_rule import PatternRule


class RecursiveFilenamePatternRule(PatternRule):
    _regex = re.compile(r'^\*/[^/\\]+\.[A-Za-z0-9]+$')

    def match(self, pattern: str) -> PatternDTO | None:
        if self._regex.fullmatch(pattern):
            return PatternDTO(
                pattern=pattern,
                value=pattern[2:],
                kind=PatternKindEnum.FILE,
                scope=PatternScopeEnum.RECURSIVE
            )

        return None
