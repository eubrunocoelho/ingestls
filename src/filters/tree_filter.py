from src.dtos.compiled_pattern_dto import CompiledPatternDTO
from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.factories.locator_factory import LocatorFactory
from src.filters.factories.matcher_factory import MatcherFactory


class TreeFilter:
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

        compiled_patterns = [
            CompiledPatternDTO(
                locator=self.locator_factory.make(pattern.scope),
                matcher=self.matcher_factory.make(pattern.kind),
                pattern=pattern,
            )
            for pattern in patterns
        ]

        self._filter(
            node=root,
            current_path='',
            compiled_patterns=compiled_patterns,
        )

        return root

    def _filter(
            self,
            node: DirectoryNode,
            current_path: str,
            compiled_patterns: list[CompiledPatternDTO],
    ) -> None:
        children: list[DirectoryNode] = []

        for child in node.children:
            child_path = (
                child.name
                if not current_path
                else f'{current_path}/{child.name}'
            )

            remove = False

            for compiled in compiled_patterns:
                if compiled.locator.matches(
                        node=child,
                        current_path=child_path,
                        matcher=compiled.matcher,
                        pattern=compiled.pattern,
                ):
                    remove = True
                    break

            if remove:
                continue

            if child.is_directory:
                self._filter(
                    node=child,
                    current_path=child_path,
                    compiled_patterns=compiled_patterns,
                )

            children.append(child)

        node.children = children
