from pathlib import Path

from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.filters.tree_filter import TreeFilter
from src.processors.pattern_set_processor import PatternSetProcessor
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy
from src.strategies.pattern_type_dispatch import STRATEGY_METHOD_BY_PATTERN_TYPE


class WindowsIngestStrategy(IngestStrategy):
    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            directory_scanner: WindowsDirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: WindowsFileReader,
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

        method_name = STRATEGY_METHOD_BY_PATTERN_TYPE.get(
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
