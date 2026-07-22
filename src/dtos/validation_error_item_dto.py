from dataclasses import dataclass
from typing import TypedDict

@dataclass(frozen=True)
class ValidationErrorItemDTO(TypedDict):
    location: list[str]
    message: str
    type: str
