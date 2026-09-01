from http import HTTPStatus

from flask import Response, request

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.responses.response_factory import ResponseFactory
from src.services.ingest_service import IngestService
from src.validators.ingest_request_validator import IngestRequestValidator
from src.validators.request_validator import RequestValidator


class IngestController:
    def __init__(self, ingest_service: IngestService):
        self.ingest_service = ingest_service

    def create(self) -> tuple[Response, int]:
        validated = RequestValidator.validate(
            IngestRequestValidator,
            request.get_json(),
        )

        dto = IngestRequestDTO(
            path=validated.path,
            pattern_type=validated.pattern_type,
            pattern=validated.pattern,
        )

        result = self.ingest_service.ingest(dto)

        return ResponseFactory.json(
            result,
            HTTPStatus.CREATED,
        )
