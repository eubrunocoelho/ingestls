from src.exceptions.business_exception import BusinessException


class DirectoryNotFoundException(BusinessException):
    def __inti__(self, path: str):
        super().__init__(
            f'O diretório `{path}` não existe.`',
            400,
        )
