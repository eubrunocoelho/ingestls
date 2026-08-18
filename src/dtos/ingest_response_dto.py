from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IngestResponseDTO:
    summary: str
    directory_structure: str
    files_content: str