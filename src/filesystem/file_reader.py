from abc import ABC, abstractmethod
from pathlib import Path

class FileReader(ABC):
    @abstractmethod
    def read(self, root: Path) -> str:
        pass
