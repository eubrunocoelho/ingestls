from dataclasses import dataclass

from src.enums.pattern_type_enum import PatternTypeEnum


@dataclass(frozen=True)
class IngestRequestDTO:
    path: str
    pattern_type: PatternTypeEnum
    pattern: str | None = None
