from dataclasses import dataclass

@dataclass(frozen=True)
class IngestRequest:
    path: str
    pattern: str | None = None
