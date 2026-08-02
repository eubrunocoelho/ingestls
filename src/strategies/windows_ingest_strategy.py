from pathlib import Path

from src.enums.pattern_type_enum import PatternTypeEnum
from src.filters.tree_filter import TreeFilter
from src.processors.pattern_set_processor import PatternSetProcessor
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.file_reader import FileReader
from src.filesystem.directory_scanner import DirectoryScanner
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class WindowsIngestStrategy(IngestStrategy):
    _STRATEGY_BY_PATTERN_TYPE = {
        PatternTypeEnum.INCLUDE: 'include',
        PatternTypeEnum.EXCLUDE: 'exclude',
    }

    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            directory_scanner: DirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: FileReader,
    ):
        self.pattern_set_processor = pattern_set_processor
        self.tree_filter = tree_filter
        self.directory_scanner = directory_scanner
        self.directory_tree_renderer = directory_tree_renderer
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return bool(Path(dto.path).drive)

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        pattern = self.pattern_set_processor.process(
            dto.pattern,
        )

        root = Path(dto.path)

        directory_tree = self.directory_scanner.read(
            root,
        )

        method_name = self._STRATEGY_BY_PATTERN_TYPE.get(
            dto.pattern_type, 'exclude'
        )
        method = getattr(self.tree_filter, method_name)

        directory_tree = method(
            root=directory_tree,
            patterns=pattern,
        )

        directory_structure = self.directory_tree_renderer.render_tree(directory_tree)

        file_content = self.file_reader.read(directory_tree)

        return IngestResponseDTO(directory_structure, file_content)
