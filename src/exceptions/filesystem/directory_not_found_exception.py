from src.exceptions.base.business_exception import BusinessException


class DirectoryNotFoundException(BusinessException):
    def __init__(self, path: str):
        super().__init__(f'Diretório não encontrado: {path}')
