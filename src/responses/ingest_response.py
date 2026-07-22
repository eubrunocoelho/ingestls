from dataclasses import dataclass


@dataclass(frozen=True)
class IngestResponse:
    message: str
