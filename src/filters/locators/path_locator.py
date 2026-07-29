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

        return matcher.matches(
            node,
            pattern,
        )
