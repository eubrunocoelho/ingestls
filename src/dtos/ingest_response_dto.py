from dataclasses import dataclass


@dataclass(frozen=True)
class IngestResponseDTO:
    directory_structure: str
    files_content: str | None = None
