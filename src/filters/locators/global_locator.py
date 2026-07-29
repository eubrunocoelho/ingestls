from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.locators.locator import Locator
from src.filters.matchers.matcher import Matcher


class GlobalLocator(Locator):
    def exclude(
            self,
            root: DirectoryNode,
            matcher: Matcher,
            pattern: PatternDTO,
            current_path: str = '',
    ) -> None:
        root.children = [
            child
            for child in root.children
            if not matcher.matches(child, pattern)
        ]
