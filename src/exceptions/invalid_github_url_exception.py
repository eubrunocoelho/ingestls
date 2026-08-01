from src.exceptions.business_exception import BusinessException


class InvalidGitHubURLException(BusinessException):
    def __init__(self, path: str):
        super().__init__(
            f'URL do GitHub inválida: {path}.',
            400,
        )
