from src.responses.ingest_response import IngestResponse
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.validators.ingest_directory_validator import IngestDirectoryValidator


class IngestService:
    def __init__(self, validator: IngestDirectoryValidator):
        self.validator = validator

    def ingest(self, dto: IngestRequestDTO) -> IngestResponse:
        self.validator.validate(dto)

        return IngestResponse(
            message='Olá, mundo!'
        )
