from src.filters.matchers.matcher import Matcher
from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode


class ExtensionMatcher(Matcher):
    def matches(
            self,
            node: DirectoryNode,
            pattern: PatternDTO,
    ) -> bool:
        if node.is_directory:
            return False

        return node.name.endswith(pattern.value)
