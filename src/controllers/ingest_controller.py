from dataclasses import asdict

from flask import jsonify, request
from pydantic import ValidationError

from src.dtos.ingest_request import IngestRequest

from src.validators.ingest_request_validator import IngestRequestValidator


class IngestController:
    @staticmethod
    def index():
        return jsonify({
            'message': 'Olá, mundo!',
        })

    @staticmethod
    def create():
        try:
            validated = IngestRequestValidator.model_validate(request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400

        dto = IngestRequest(
            path=validated.path,
            pattern=validated.pattern,
        )

        return jsonify(asdict(dto)), 201
