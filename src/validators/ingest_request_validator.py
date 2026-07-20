from pydantic import BaseModel, ConfigDict

class IngestRequestValidator(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    pattern: str | None = None
