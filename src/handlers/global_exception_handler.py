from flask import jsonify, Flask, Response
from pydantic import ValidationError

from src.exceptions.business_exception import BusinessException
from src.responses.validation_error_response import ValidationErrorResponse


class GlobalExceptionHandler:
    @staticmethod
    def init_app(app: Flask) -> None:
        app.register_error_handler(
            ValidationError,
            GlobalExceptionHandler.handle_validation_error,
        )

        app.register_error_handler(
            BusinessException,
            GlobalExceptionHandler.handle_business_exception,
        )

    @staticmethod
    def handle_validation_error(
            e: ValidationError,
    ) -> tuple[Response, int]:
        response = ValidationErrorResponse.from_pydantic(e)

        return jsonify(response.to_dict()), 400

    @staticmethod
    def handle_business_exception(
            e: BusinessException,
    ) -> tuple[Response, int]:
        return jsonify({
            'message': str(e),
        }), e.status_code
