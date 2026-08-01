import re

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.invalid_github_url_exception import InvalidGitHubURLException
from src.validators.directory_rules.ingest_rule import IngestRule

GITHUB_URL_PATTERN = re.compile(
    r'^https://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)/?$'
)


class GitHubURLFormatRule(IngestRule):
    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith('https://github.com/')

    def validate(self, dto: IngestRequestDTO) -> None:
        if GITHUB_URL_PATTERN.match(dto.path) is None:
            raise InvalidGitHubURLException(dto.path)
