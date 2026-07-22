from pathlib import Path

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.readers.file_reader import FileReader


class WindowsFileReader(FileReader):
    def read(self, dto: IngestRequestDTO) -> str:
        directory = Path(dto.path)

        contents = []

        for file in directory.rglob("*"):
            if file.is_file():
                contents.append(
                    f'===== {file.name} =====\n'
                )

                contents.append(
                    file.read_text(
                        encoding='utf-8',
                    )
                )

        return '\n'.join(contents)
