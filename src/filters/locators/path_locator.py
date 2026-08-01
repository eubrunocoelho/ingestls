from dataclasses import replace

from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.locators.locator import Locator
from src.filters.matchers.matcher import Matcher


class PathLocator(Locator):
    def matches(
            self,
            node: DirectoryNode,
            current_path: str,
            matcher: Matcher,
            pattern: PatternDTO,
    ) -> bool:
        if current_path != pattern.value:
            return False

        local_pattern = replace(pattern, value=node.name)

        return matcher.matches(
            node,
            local_pattern,
        )
