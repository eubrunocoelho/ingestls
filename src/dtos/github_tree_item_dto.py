from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GitHubTreeItemDTO:
    path: str
    type: str
    sha: str
    size: int | None
