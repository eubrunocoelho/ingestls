from pathlib import Path

from src.filesystem.directory_node import DirectoryNode


class WindowsDirectoryScanner:
    _IGNORED_DIRECTORIES = {'.git'}

    def read(self, root: Path) -> DirectoryNode:
        return self._build(root)

    def _build(self, root: Path) -> DirectoryNode:
        node = DirectoryNode(
            name=root.name if root.name else str(root),
            is_directory=root.is_dir(),
            path=str(root),
        )

        if not root.is_dir():
            return node

        children = sorted(
            (
                child
                for child in root.iterdir()
                if not (
                    child.is_dir() and child.name in self._IGNORED_DIRECTORIES
            )
            ),
            key=lambda p: (
                p.is_file(),
                p.name.lower(),
            ),
        )

        for child in children:
            node.children.append(self._build(child))

        return node
