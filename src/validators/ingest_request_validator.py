from pathlib import PureWindowsPath
from pydantic import BaseModel, ConfigDict, field_validator


class IngestRequestValidator(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    pattern: str | None = None

    @field_validator("path")
    @classmethod
    def validate_path(cls: type["IngestRequestValidator"], value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("O campo `path` é obrigatório.")

        path = PureWindowsPath(value)

        if not path.drive:
            raise ValueError("O caminho deve iniciar com uma unidade válida (ex.: C:\\).")

        return value
