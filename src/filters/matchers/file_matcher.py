from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode


class FileMatcher:
    def matches(
            self,
            node: DirectoryNode,
            pattern: PatternDTO,
    ) -> bool:
        return (
                not node.is_directory
                and node.name == pattern.pattern
        )
