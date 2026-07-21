from typing import TypedDict


class ValidationErrorItem(TypedDict):
    location: list[str]
    message: str
    type: str
