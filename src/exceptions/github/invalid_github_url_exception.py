from src.exceptions.base.business_exception import BusinessException


class InvalidGitHubURLException(BusinessException):
    def __init__(self, url: str):
        super().__init__(f'URL do GitHub inválida: {url}')
