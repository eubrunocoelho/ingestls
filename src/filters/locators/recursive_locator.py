from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.matcher import Matcher
from src.filters.locators.locator import Locator


class RecursiveLocator(Locator):
    def matches(
            self,
            node: DirectoryNode,
            current_path: str,
            matcher: Matcher,
            pattern: PatternDTO,
    ) -> bool:
        return matcher.matches(
            node,
            pattern,
        )
