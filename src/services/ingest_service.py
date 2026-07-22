from src.dtos.ingest_response_dto import IngestResponseDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.validators.ingest_directory_validator import IngestDirectoryValidator


class IngestService:
    def __init__(self, validator: IngestDirectoryValidator):
        self.validator = validator

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        self.validator.validate(dto)

        return IngestResponseDTO(
            message='Olá, mundo!'
        )
