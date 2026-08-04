from dataclasses import dataclass

from src.enums.pattern_type_enum import PatternTypeEnum


@dataclass(frozen=True, slots=True)
class IngestRequestDTO:
    path: str
    pattern_type: PatternTypeEnum = PatternTypeEnum.EXCLUDE
    pattern: str | None = None
