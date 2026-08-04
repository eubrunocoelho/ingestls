from typing import TypedDict

class ValidationErrorItemDTO(TypedDict):
    location: list[str]
    message: str
    type: str
