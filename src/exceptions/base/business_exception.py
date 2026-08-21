from http import HTTPStatus


class BusinessException(Exception):
    def __init__(self, message: str, status_code: HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY) -> None:
        super().__init__(message)

        self.status_code = status_code
