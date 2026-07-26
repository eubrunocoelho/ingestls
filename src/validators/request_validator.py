from typing import TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class RequestValidator:
    @staticmethod
    def validate(model: type[T], data: dict) -> T:
        return model.model_validate(data)
