from pathlib import Path

from src.providers.ingest_summary_provider import IngestSummaryProvider
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.filters.tree_filter import TreeFilter
from src.processors.pattern_set_processor import PatternSetProcessor
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class WindowsIngestStrategy(IngestStrategy[Path]):
    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            directory_scanner: WindowsDirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: WindowsFileReader,
            ingest_summary_provider: IngestSummaryProvider,
    ):
        super().__init__(pattern_set_processor, tree_filter, directory_tree_renderer, ingest_summary_provider)
        self.directory_scanner = directory_scanner
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return bool(Path(dto.path).drive)

    def _resolve_target(self, dto: IngestRequestDTO) -> Path:
        return Path(dto.path)

    def _scan(self, target: Path) -> DirectoryNode:
        return self.directory_scanner.read(target)

    def _read_files(self, target: Path, directory_tree: DirectoryNode) -> str:
        return self.file_reader.read(directory_tree)

    def _describe_target(self, target: Path) -> str:
        return target.name if target.name else str(target)
