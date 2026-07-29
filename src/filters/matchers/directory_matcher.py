from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode


class DirectoryMatcher:
    def matches(
            self,
            node: DirectoryNode,
            pattern: PatternDTO,
    ) -> bool:
        return (
                node.is_directory
                and node.name == pattern.pattern.rstrip('/')
        )
