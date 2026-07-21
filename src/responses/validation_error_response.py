from dataclasses import asdict, dataclass, field

from pydantic import ValidationError


@dataclass(slots=True)
class ValidationErrorResponse:
    errors: list[dict[str, str | list[str]]] = field(default_factory=list)

    @classmethod
    def from_pydantic(
            cls,
            exception: ValidationError,
    ) -> "ValidationErrorResponse":
        return cls(
            errors=[
                {
                    "location": [str(value) for value in error["loc"]],
                    "message": error["msg"],
                    "type": error["type"],
                }
                for error in exception.errors()
            ]
        )

    def to_dict(self) -> dict:
        return asdict(self)
