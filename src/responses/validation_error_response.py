from dataclasses import asdict, dataclass, field
from typing import ClassVar

from pydantic import ValidationError

from src.dtos.validation_error_item_dto import ValidationErrorItemDTO


@dataclass(frozen=True, slots=True)
class ValidationErrorResponse:
    _ERROR_MESSAGES: ClassVar[
        dict[str, str]
    ] = {
        'missing': 'O campo é obrigatório.',
        'extra_forbidden': 'Campo não permitido.',
        'string_type': 'O campo deve ser uma string.',
        'string_too_short': 'O campo não pode ser vazio.',
    }

    errors: list[ValidationErrorItemDTO] = field(default_factory=list)

    @classmethod
    def from_pydantic(
            cls,
            e: ValidationError,
    ) -> "ValidationErrorResponse":
        errors: list[ValidationErrorItemDTO] = []

        for error in e.errors():
            errors.append(
                {
                    'location': [str(value) for value in error['loc']],
                    'message': cls._ERROR_MESSAGES.get(
                        error['type'],
                        error['msg'],
                    ),
                    'type': error['type'],
                }
            )

        return cls(errors=errors)

    def to_dict(self) -> dict[str, list[ValidationErrorItemDTO]]:
        return asdict(self)
