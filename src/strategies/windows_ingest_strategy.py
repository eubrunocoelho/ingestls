from pathlib import Path

from src.readers.file_reader import FileReader
from src.readers.directory_reader import DirectoryReader
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class WindowsIngestStrategy(IngestStrategy):
    def __init__(
            self,
            reader: DirectoryReader,
            file_reader: FileReader,
    ):
        self.reader = reader
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return bool(Path(dto.path).drive)

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        structure = self.reader.read(dto)
        content = self.file_reader.read(dto)

        return IngestResponseDTO(
            directory_structure=structure,
            files_content=content,
        )
