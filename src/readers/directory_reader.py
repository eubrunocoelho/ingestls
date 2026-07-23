from abc import ABC, abstractmethod
from pathlib import Path

from src.models.directory_node import DirectoryNode


class DirectoryReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> DirectoryNode:
        pass
