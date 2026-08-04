from pathlib import Path

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.filesystem.directory_not_found_exception import DirectoryNotFoundException
from src.exceptions.filesystem.invalid_directory_exception import InvalidDirectoryException
from src.validators.directory_rules.ingest_rule import IngestRule


class DirectoryExistsRule(IngestRule):
    def supports(self, dto: IngestRequestDTO) -> bool:
        return bool(Path(dto.path).drive)

    def validate(self, dto: IngestRequestDTO) -> None:
        path = Path(dto.path)

        if not path.exists():
            raise DirectoryNotFoundException(dto.path)

        if not path.is_dir():
            raise InvalidDirectoryException(dto.path)
