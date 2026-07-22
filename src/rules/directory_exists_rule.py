from pathlib import Path

from src.exceptions.invalid_directory_exception import InvalidDirectoryException
from src.exceptions.directory_not_found_exception import DirectoryNotFoundException
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.rules.ingest_rule import IngestRule


class DirectoryExistsRule(IngestRule):
    def validate(self, dto: IngestRequestDTO) -> None:
        path = Path(dto.path)

        if not path.exists():
            raise DirectoryNotFoundException(dto.path)

        if not path.is_dir():
            raise InvalidDirectoryException(dto.path)
