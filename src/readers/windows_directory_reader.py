from pathlib import Path

from src.models.directory_node import DirectoryNode
from src.readers.directory_reader import DirectoryReader


class WindowsDirectoryReader(DirectoryReader):
    def read(self, path: Path) -> DirectoryNode:
        return self._build(path)

    def _build(self, path: Path) -> DirectoryNode:
        node = DirectoryNode(
            name=path.name if path.name else str(path),
            is_directory=path.is_dir(),
        )

        if not path.is_dir():
            return node

        children = sorted(
            path.iterdir(),
            key=lambda p: (
                p.is_file(),
                p.name.lower(),
            ),
        )

        for child in children:
            node.children.append(self._build(child))

        return node
