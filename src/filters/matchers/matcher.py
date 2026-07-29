from abc import ABC, abstractmethod

from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode


class Matcher(ABC):
    @abstractmethod
    def matches(
            self,
            node: DirectoryNode,
            pattern: PatternDTO
    ) -> bool:
        pass
