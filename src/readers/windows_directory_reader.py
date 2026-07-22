from pathlib import Path

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.readers.directory_reader import DirectoryReader


class WindowsDirectoryReader(DirectoryReader):
    def read(self, dto: IngestRequestDTO) -> str:
        directory = Path(dto.path)

        structure = []

        for item in directory.rglob('*'):
            structure.append(str(item))

        return '\n'.join(structure)
