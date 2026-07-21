from flask import jsonify, Flask, Response
from pydantic import ValidationError

from src.responses.validation_error_response import ValidationErrorResponse


class GlobalExceptionHandler:
    @staticmethod
    def init_app(app: Flask) -> None:
        app.register_error_handler(
            ValidationError,
            GlobalExceptionHandler.handle_validation_error,
        )

    @staticmethod
    def handle_validation_error(
            e: ValidationError,
    ) -> tuple[Response, int]:
        response = ValidationErrorResponse.from_pydantic(e)

        return jsonify(response.to_dict()), 400
