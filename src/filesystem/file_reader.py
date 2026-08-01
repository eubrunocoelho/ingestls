from abc import ABC, abstractmethod

from src.filesystem.directory_node import DirectoryNode


class FileReader(ABC):
    @abstractmethod
    def read(self, tree: DirectoryNode) -> str:
        pass
