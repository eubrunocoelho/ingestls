from dataclasses import dataclass

from src.enums.github_url_type_enum import GitHubURLTypeEnum


@dataclass(frozen=True, slots=True)
class GitHubURLDTO:
    url: str
    owner: str
    repository: str
    type: GitHubURLTypeEnum
    reference: str | None = None
    path: str | None = None
