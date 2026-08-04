from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IngestResponseDTO:
    directory_structure: str
    files_content: str
