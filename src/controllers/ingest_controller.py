from dataclasses import asdict

from flask import jsonify, request, Response

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.validators.ingest_request_validator import IngestRequestValidator
from src.validators.request_validator import RequestValidator
from src.services.ingest_service import IngestService


class IngestController:
    def __init__(self, ingest_service: IngestService):
        self.ingest_service = ingest_service

    def index(self) -> Response:
        return jsonify({
            'message': 'Olá, mundo!',
        })

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

        return jsonify(asdict(result)), 201
