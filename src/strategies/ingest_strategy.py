from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filters.tree_filter import TreeFilter
from src.processors.pattern_set_processor import PatternSetProcessor
from src.strategies.pattern_type_dispatch import STRATEGY_METHOD_BY_PATTERN_TYPE

TTarget = TypeVar('TTarget')


class IngestStrategy(ABC, Generic[TTarget]):
    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            directory_tree_renderer: DirectoryTreeRenderer,
    ):
        self.pattern_set_processor = pattern_set_processor
        self.tree_filter = tree_filter
        self.directory_tree_renderer = directory_tree_renderer

    @abstractmethod
    def supports(self, dto: IngestRequestDTO) -> bool:
        pass

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        pattern = self.pattern_set_processor.process(dto.pattern)
        target = self._resolve_target(dto)

        try:
            directory_tree = self._scan(target)

            method_name = STRATEGY_METHOD_BY_PATTERN_TYPE.get(
                dto.pattern_type, 'exclude'
            )
            method = getattr(self.tree_filter, method_name)

            directory_tree = method(
                root=directory_tree,
                patterns=pattern
            )

            directory_structure = self.directory_tree_renderer.render_tree(directory_tree)
            file_content = self._read_files(target, directory_tree)

            return IngestResponseDTO(directory_structure, file_content)
        finally:
            self._cleanup(target)

    @abstractmethod
    def _resolve_target(self, dto: IngestRequestDTO) -> TTarget:
        pass

    @abstractmethod
    def _scan(self, target: TTarget) -> DirectoryNode:
        pass

    @abstractmethod
    def _read_files(self, target: TTarget, directory_tree: DirectoryNode) -> str:
        pass

    def _cleanup(self, target: TTarget) -> None:
        pass
