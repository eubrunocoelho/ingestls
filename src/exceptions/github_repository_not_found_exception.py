from src.exceptions.business_exception import BusinessException


class GitHubRepositoryNotFoundException(BusinessException):
    def __init__(self, path: str):
        super().__init__(
            f'Repositório do GitHub não encontrado: {path}',
            400,
        )
