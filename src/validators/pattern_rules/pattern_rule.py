from abc import ABC, abstractmethod

from src.dtos.pattern_dto import PatternDTO


class PatternRule(ABC):
    @abstractmethod
    def match(self, pattern: str) -> PatternDTO | None:
        pass
