from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.locators.locator import Locator
from src.filters.matchers.matcher import Matcher


class PathLocator(Locator):
    def exclude(
            self,
            root: DirectoryNode,
            matcher: Matcher,
            pattern: PatternDTO,
            current_path: str = '',
    ) -> None:
        children = []

        for child in root.children:
            path = (
                child.name
                if not current_path
                else f'{current_path}/{child.name}'
            )

            if (
                    matcher.matches(child, pattern)
                    and path == pattern.pattern
            ):
                continue

            if child.is_directory:
                self.exclude(
                    child,
                    matcher,
                    pattern,
                    path,
                )

            children.append(child)

        root.children = children
