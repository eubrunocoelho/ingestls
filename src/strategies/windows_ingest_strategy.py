from pathlib import Path

from src.formatters.ascii_directory_tree_formatter import AsciiDirectoryTreeFormatter
from src.readers.file_reader import FileReader
from src.readers.directory_reader import DirectoryReader
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class WindowsIngestStrategy(IngestStrategy):
    def __init__(
            self,
            directory_reader: DirectoryReader,
            tree_formatter: AsciiDirectoryTreeFormatter,
            file_reader: FileReader,
    ):
        self.directory_reader = directory_reader
        self.tree_formatter = tree_formatter
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return bool(Path(dto.path).drive)

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        tree = self.directory_reader.read(
            Path(dto.path),
        )

        structure = self.tree_formatter.format(tree)

        content = self.file_reader.read(dto)

        return IngestResponseDTO(structure, content)
