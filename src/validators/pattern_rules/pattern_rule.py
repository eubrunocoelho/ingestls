from abc import ABC, abstractmethod

from src.enums.pattern_kind_enum import PatternKindEnum


class PatternRule(ABC):
    @abstractmethod
    def match(self, pattern: str) -> PatternKindEnum | None:
        pass
