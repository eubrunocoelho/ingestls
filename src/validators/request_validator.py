from typing import Type
from pydantic import BaseModel


class RequestValidator:
    @staticmethod
    def validate(model: Type[BaseModel], data: dict):
        return model.model_validate(data)
