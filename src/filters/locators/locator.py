from abc import ABC, abstractmethod

from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.matcher import Matcher


class Locator(ABC):
    @abstractmethod
    def matches(
            self,
            node: DirectoryNode,
            current_path: str,
            matcher: Matcher,
            pattern: PatternDTO,
    ) -> bool:
        pass
