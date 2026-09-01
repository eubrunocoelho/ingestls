from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.validators.ingest_directory_validator import IngestDirectoryValidator


class IngestService:
    def __init__(self, validator: IngestDirectoryValidator, dispatcher: IngestDispatcher):
        self.validator = validator
        self.dispatcher = dispatcher

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        self.validator.validate(dto)

        return self.dispatcher.dispatch(dto)
