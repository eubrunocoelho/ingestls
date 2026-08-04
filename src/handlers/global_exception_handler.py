import logging

from flask import jsonify, Flask, Response
from pydantic import ValidationError

from src.exceptions.base.business_exception import BusinessException
from src.exceptions.base.infrastructure_exception import InfrastructureException
from src.exceptions.dump.debug_exception import DumpException
from src.responses.debug_response import DebugResponse
from src.responses.validation_error_response import ValidationErrorResponse

logger = logging.getLogger(__name__)


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

        app.register_error_handler(
            InfrastructureException,
            GlobalExceptionHandler.handle_infrastructure_exception,
        )

        app.register_error_handler(
            DumpException,
            GlobalExceptionHandler.handle_dump_exception,
        )

        app.register_error_handler(
            Exception,
            GlobalExceptionHandler.handle_unexpected_exception,
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

    @staticmethod
    def handle_infrastructure_exception(
            e: InfrastructureException,
    ) -> tuple[Response, int]:
        logger.exception(e)

        return jsonify({
            'message': 'Ocorreu um erro interno durante o processamento da solicitação.',
        }), e.status_code

    @staticmethod
    def handle_dump_exception(
            e: DumpException,
    ) -> Response:
        return Response(
            DebugResponse.to_html(e.value),
            mimetype='text/html',
            status=200,
        )

    @staticmethod
    def handle_unexpected_exception(
            e: Exception,
    ) -> tuple[Response, int]:
        logger.exception(e)

        return jsonify({
            'message': 'Ocorreu um erro inesperado.',
        }), 500
