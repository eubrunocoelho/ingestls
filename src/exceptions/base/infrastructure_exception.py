class InfrastructureException(Exception):
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
