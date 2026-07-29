from dataclasses import dataclass

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum


@dataclass(frozen=True, slots=True)
class PatternDTO:
    pattern: str
    value: str
    kind: PatternKindEnum
    scope: PatternScopeEnum
