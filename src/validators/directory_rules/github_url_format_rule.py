from src.integrations.github_constants import GITHUB_URL_PATTERN, GITHUB_URL_PREFIX
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.github.invalid_github_url_exception import InvalidGitHubURLException
from src.validators.directory_rules.ingest_rule import IngestRule


class GitHubURLFormatRule(IngestRule):
    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith(GITHUB_URL_PREFIX)

    def validate(self, dto: IngestRequestDTO) -> None:
        if GITHUB_URL_PATTERN.fullmatch(dto.path) is None:
            raise InvalidGitHubURLException(dto.path)
