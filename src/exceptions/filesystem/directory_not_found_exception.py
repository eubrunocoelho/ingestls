from http import HTTPStatus

from src.exceptions.base.business_exception import BusinessException


class DirectoryNotFoundException(BusinessException):
    def __init__(self, path: str):
        super().__init__(
            message=f'Diretório não encontrado: {path}',
            status_code=HTTPStatus.NOT_FOUND,
        )
