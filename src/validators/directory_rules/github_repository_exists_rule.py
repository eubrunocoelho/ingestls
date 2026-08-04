from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.github.github_repository_not_found_exception import GitHubRepositoryNotFoundException
from src.integrations.github_client import GitHubClient
from src.validators.directory_rules.github_url_format_rule import GITHUB_URL_PATTERN, GITHUB_URL_PREFIX
from src.validators.directory_rules.ingest_rule import IngestRule


class GitHubRepositoryExistsRule(IngestRule):
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith(GITHUB_URL_PREFIX)

    def validate(self, dto: IngestRequestDTO) -> None:
        match = GITHUB_URL_PATTERN.match(dto.path.rstrip('/'))

        if match is None:
            return

        owner, repo = match.group('owner'), match.group('repo')

        if not self.github_client.repository_exists(owner, repo):
            raise GitHubRepositoryNotFoundException(dto.path)
