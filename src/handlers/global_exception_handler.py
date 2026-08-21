import logging
import traceback
from http import HTTPStatus

from flask import Flask, Response
from pydantic import ValidationError

from src.exceptions.base.business_exception import BusinessException
from src.exceptions.base.infrastructure_exception import InfrastructureException
from src.exceptions.dump.debug_exception import DumpException
from src.responses.debug_response import DebugResponse
from src.responses.response_factory import ResponseFactory
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
    def _log_exception(e: Exception) -> None:
        logger.exception(e)

    @staticmethod
    def _get_stacktrace(e: Exception) -> str:
        return ''.join(
            traceback.format_exception(
                type(e),
                e,
                e.__traceback__,
            )
        )

    @staticmethod
    def handle_validation_error(
            e: ValidationError,
    ) -> tuple[Response, int]:
        response = ValidationErrorResponse.from_pydantic(e)

        return ResponseFactory.json(
            response,
            HTTPStatus.BAD_REQUEST,
        )

    @staticmethod
    def handle_business_exception(
            e: BusinessException,
    ) -> tuple[Response, int]:
        GlobalExceptionHandler._log_exception(e)

        return ResponseFactory.json(
            {
                'message': str(e) or (
                    'Ocorreu um erro interno durante o '
                    'processamento da solicitação.'
                ),
                'stacktrace': GlobalExceptionHandler._get_stacktrace(e),
            },
            HTTPStatus(e.status_code)
        )

    @staticmethod
    def handle_infrastructure_exception(
            e: InfrastructureException,
    ) -> tuple[Response, int]:
        GlobalExceptionHandler._log_exception(e)

        return ResponseFactory.json(
            {
                'message': str(e) or (
                    'Ocorreu um erro interno durante o '
                    'processamento da solicitação.'
                ),
                'stacktrace': GlobalExceptionHandler._get_stacktrace(e),
            },
            HTTPStatus(e.status_code)
        )

    @staticmethod
    def handle_unexpected_exception(
            e: Exception,
    ) -> tuple[Response, int]:
        GlobalExceptionHandler._log_exception(e)

        return ResponseFactory.json(
            {
                'message': 'Ocorreu um erro inesperado.',
                'stacktrace': GlobalExceptionHandler._get_stacktrace(e),
            },
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

    @staticmethod
    def handle_dump_exception(
            e: DumpException,
    ) -> Response:
        return Response(
            DebugResponse.to_html(e.value),
            mimetype='text/html',
            status=200,
        )
