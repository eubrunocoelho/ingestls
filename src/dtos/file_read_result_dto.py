from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FileReadResultDTO:
    content: str
    code_line_count: int
