from pathlib import Path

from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.file_reader import FileReader
from src.filesystem.directory_scanner import DirectoryScanner
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class WindowsIngestStrategy(IngestStrategy):
    def __init__(
            self,
            directory_scanner: DirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: FileReader,
    ):
        self.directory_scanner = directory_scanner
        self.directory_tree_renderer = directory_tree_renderer
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return bool(Path(dto.path).drive)

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        tree = self.directory_scanner.read(
            Path(dto.path),
        )

        structure = self.directory_tree_renderer.render_tree(tree)

        content = self.file_reader.read(dto)

        return IngestResponseDTO(structure, content)
