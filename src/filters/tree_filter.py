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
        compiled_patterns = self._compile(patterns)

        self._filter_exclude(
            node=root,
            current_path='',
            compiled_patterns=compiled_patterns,
        )

        return root

    def include(
            self,
            root: DirectoryNode,
            patterns: list[PatternDTO],
    ) -> DirectoryNode:
        compiled_patterns = self._compile(patterns)

        self._filter_include(
            node=root,
            current_path='',
            compiled_patterns=compiled_patterns,
        )

        return root

    def _compile(
            self,
            patterns: list[PatternDTO],
    ) -> list[CompiledPatternDTO]:
        return [
            CompiledPatternDTO(
                locator=self.locator_factory.make(pattern.scope),
                matcher=self.matcher_factory.make(pattern.kind),
                pattern=pattern,
            )
            for pattern in patterns
        ]

    @staticmethod
    def _matches_any(
            node: DirectoryNode,
            current_path: str,
            compiled_patterns: list[CompiledPatternDTO],
    ) -> bool:
        return any(
            compiled.locator.matches(
                node=node,
                current_path=current_path,
                matcher=compiled.matcher,
                pattern=compiled.pattern,
            )
            for compiled in compiled_patterns
        )

    def _filter_exclude(
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

            if self._matches_any(child, child_path, compiled_patterns):
                continue

            if child.is_directory:
                self._filter_exclude(
                    node=child,
                    current_path=child_path,
                    compiled_patterns=compiled_patterns,
                )

            children.append(child)

        node.children = children

    def _filter_include(
            self,
            node: DirectoryNode,
            current_path: str,
            compiled_patterns: list[CompiledPatternDTO],
    ) -> bool:
        # Filtra `node.children` in-place, mantendo só o que bate em algum padrão (arquivos)
        # ou contém algo que bate (diretórios). Retorna `True` se `node` deve ser mantido pelo
        # pai (batou direto ou sobrou algo dentro dele)
        kept_children: list[DirectoryNode] = []

        for child in node.children:
            child_path = (
                child.name
                if not current_path
                else f'{current_path}/{child.name}'
            )

            matched = self._matches_any(child, child_path, compiled_patterns)

            if child.is_directory:
                if matched:
                    # Padrão de diretório beteu direto: mantém a subárvore
                    # intera, sem filtrar recursivamente por dentro.
                    kept_children.append(child)
                    continue

                has_kept_descendant = self._filter_include(
                    node=child,
                    current_path=child_path,
                    compiled_patterns=compiled_patterns,
                )

                if has_kept_descendant:
                    kept_children.append(child)

            else:
                if matched:
                    kept_children.append(child)

        node.children = kept_children

        return bool(kept_children)
