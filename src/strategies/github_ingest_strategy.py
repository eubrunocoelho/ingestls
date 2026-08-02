from src.dtos.ingest_request_dto import IngestRequestDTO
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.filesystem.github_directory_scanner import GitHubDirectoryScanner
from src.strategies.ingest_strategy import IngestStrategy
from src.validators.directory_rules.github_url_format_rule import GITHUB_URL_PATTERN


class GitHubIngestStrategy(IngestStrategy):
    def __init__(
            self,
            directory_scanner: GitHubDirectoryScanner,
    ):
        self.directory_scanner = directory_scanner

    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith('https://github.com/')

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        match = GITHUB_URL_PATTERN.match(dto.path.rstrip('/'))
        owner, repo = match.group('owner'), match.group('repo')

        directory_tree = self.directory_scanner.read(owner, repo)

        # NOT IMPLEMENTED
