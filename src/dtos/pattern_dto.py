from dataclasses import dataclass

from src.enums.pattern_kind_enum import PatternKindEnum


@dataclass(frozen=True, slots=True)
class PatternDTO:
    pattern: str
    kind: PatternKindEnum
