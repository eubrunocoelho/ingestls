from src.exceptions.base.business_exception import BusinessException


class InvalidDirectoryException(BusinessException):
    def __init__(self, path: str):
        super().__init__(f'{path} não é um diretório.')
