from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode


class ExtensionMatcher:
    def matches(
            self,
            node: DirectoryNode,
            pattern: PatternDTO,
    ) -> bool:
        if node.is_directory:
            return False

        return node.name.endswith(
            pattern.pattern[1:]
        )
