from pathlib import Path

from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_scanner import DirectoryScanner


class WindowsDirectoryScanner(DirectoryScanner):
    def read(self, root: Path) -> DirectoryNode:
        return self._build(root)

    def _build(self, root: Path) -> DirectoryNode:
        node = DirectoryNode(
            name=root.name if root.name else str(root),
            is_directory=root.is_dir(),
        )

        if not root.is_dir():
            return node

        children = sorted(
            root.iterdir(),
            key=lambda p: (
                p.is_file(),
                p.name.lower(),
            )
        )

        for child in children:
            node.children.append(self._build(child))

        return node
