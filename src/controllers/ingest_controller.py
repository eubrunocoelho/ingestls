from dataclasses import asdict

from flask import jsonify, request

from src.dtos.ingest_request import IngestRequest
from src.validators.ingest_request_validator import IngestRequestValidator
from src.validators.request_validator import RequestValidator


class IngestController:
    @staticmethod
    def index():
        return jsonify({
            'message': 'Olá, mundo!',
        })

    @staticmethod
    def create():
        validated = RequestValidator.validate(
            IngestRequestValidator,
            request.get_json(),
        )

        dto = IngestRequest(
            path=validated.path,
            pattern=validated.pattern,
        )

        return jsonify(asdict(dto)), 201
