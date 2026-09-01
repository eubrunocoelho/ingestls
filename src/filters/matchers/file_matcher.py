from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.matcher import Matcher


class FileMatcher(Matcher):
    def matches(
            self,
            node: DirectoryNode,
            pattern: PatternDTO,
    ) -> bool:
        return (
                not node.is_directory
                and node.name == pattern.value
        )
