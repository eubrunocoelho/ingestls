from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GitHubURLPartsDTO:
    url: str
    owner: str
    repository: str
    segments: tuple[str, ...]
