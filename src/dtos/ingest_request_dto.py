from dataclasses import dataclass

@dataclass(frozen=True)
class IngestRequestDTO:
    path: str
    pattern: str | None = None
