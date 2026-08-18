from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

from src.providers.ingest_summary_provider import IngestSummaryProvider
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
            ingest_summary_provider: IngestSummaryProvider,
    ):
        self.pattern_set_processor = pattern_set_processor
        self.tree_filter = tree_filter
        self.directory_tree_renderer = directory_tree_renderer
        self.ingest_summary_provider = ingest_summary_provider

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

            summary = self.ingest_summary_provider.build(
                target_label=self._describe_target(target),
                directory_tree=directory_tree,
                directory_structure=directory_structure,
                files_content=file_content,
            )

            return IngestResponseDTO(summary, directory_structure, file_content)
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

    def _describe_target(self, target: TTarget) -> str:
        pass

    def _cleanup(self, target: TTarget) -> None:
        pass
