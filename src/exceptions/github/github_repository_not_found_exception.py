from src.exceptions.base.business_exception import BusinessException


class GitHubRepositoryNotFoundException(BusinessException):
    def __init__(self, repository: str):
        super().__init__(f'Repositório não encontrado: {repository}')
