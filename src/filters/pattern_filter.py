from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.factories.locator_factory import LocatorFactory
from src.filters.factories.matcher_factory import MatcherFactory


class PatternFilter:
    def __init__(
            self,
            locator_factory: LocatorFactory,
            matcher_factory: MatcherFactory,
    ):
        self.locator_factory = locator_factory
        self.matcher_factory = matcher_factory

    def exclude(
            self,
            root: DirectoryNode,
            patterns: list[PatternDTO],
    ) -> DirectoryNode:
        for pattern in patterns:
            locator = self.locator_factory.make(pattern.scope)
            matcher = self.matcher_factory.make(pattern.kind)

            locator.exclude(
                root,
                matcher,
                pattern,
            )

        return root
