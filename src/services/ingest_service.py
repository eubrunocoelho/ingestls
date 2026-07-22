from src.responses.ingest_response import IngestResponse
from src.dtos.ingest_request import IngestRequest
from src.validators.ingest_directory_validator import IngestDirectoryValidator


class IngestService:
    def __init__(self, validator: IngestDirectoryValidator):
        self.validator = validator

    def ingest(self, dto: IngestRequest) -> IngestResponse:
        self.validator.validate(dto)

        return IngestResponse(
            message='Olá, mundo!'
        )
