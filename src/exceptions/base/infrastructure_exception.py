from http import HTTPStatus


class InfrastructureException(Exception):
    def __init__(self, message: str, status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR):
        super().__init__(message)

        self.status_code = status_code
