import re

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.pattern_rule import PatternRule


class DirectoryPatternRule(PatternRule):
    _regex = re.compile(r'^[A-Za-z0-9._-]+/$')

    def match(self, pattern: str) -> PatternDTO | None:
        if self._regex.fullmatch(pattern):
            return PatternDTO(
                pattern=pattern,
                value=pattern[:-1],
                kind=PatternKindEnum.DIRECTORY,
                scope=PatternScopeEnum.GLOBAL,
            )

        return None
