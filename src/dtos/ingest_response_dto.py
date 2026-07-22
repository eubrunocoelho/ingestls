from dataclasses import dataclass


@dataclass(frozen=True)
class IngestResponseDTO:
    message: str
