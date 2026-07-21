from dataclasses import asdict, dataclass, field

from pydantic import ValidationError

ERROR_MESSAGES = {
    'missing': 'O campo é obrigatório.',
    'extra_forbidden': 'Campo não permitido.',
    'string_type': 'O campo deve ser uma string.',
    'string_too_short': 'O campo não pode ser vazio.',
}


@dataclass(slots=True)
class ValidationErrorResponse:
    errors: list[dict[str, str | list[str]]] = field(default_factory=list)

    @classmethod
    def from_pydantic(
            cls,
            exception: ValidationError,
    ) -> "ValidationErrorResponse":
        errors = []

        for error in exception.errors():
            errors.append(
                {
                    'location': [str(value) for value in error['loc']],
                    'message': ERROR_MESSAGES.get(
                        error['type'],
                        error['msg'],
                    ),
                    'type': error['type'],
                }
            )

        return cls(errors=errors)

    def to_dict(self) -> dict:
        return asdict(self)
