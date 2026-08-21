from dataclasses import dataclass

from src.filesystem.directory_node import DirectoryNode


@dataclass(frozen=True, slots=True)
class DirectoryTreeStats:
    directory_count: int
    file_count: int

    @classmethod
    def from_tree(cls, root: DirectoryNode) -> 'DirectoryTreeStats':
        directory_count = 0
        file_count = 0

        for child in root.children:
            if child.is_directory:
                directory_count += 1
                nested = cls.from_tree(child)
                directory_count += nested.directory_count
                file_count += nested.file_count
            else:
                file_count += 1

        return cls(directory_count=directory_count, file_count=file_count)
