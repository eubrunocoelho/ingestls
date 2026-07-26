from abc import ABC, abstractmethod
from pathlib import Path

from src.filesystem.directory_node import DirectoryNode


class DirectoryScanner(ABC):
    @abstractmethod
    def read(self, root: Path) -> DirectoryNode:
        pass
