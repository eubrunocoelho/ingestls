from http import HTTPStatus

from src.exceptions.base.business_exception import BusinessException


class InvalidGitHubURLException(BusinessException):
    def __init__(self, url: str):
        super().__init__(
            message=f'URL do GitHub inválida: {url}',
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )
