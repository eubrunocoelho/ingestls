from http import HTTPStatus

from src.exceptions.base.business_exception import BusinessException


class InvalidDirectoryException(BusinessException):
    def __init__(self, path: str):
        super().__init__(
            message=f'{path} não é um diretório.',
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )
