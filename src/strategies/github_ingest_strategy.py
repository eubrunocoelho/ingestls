from pathlib import Path

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.github.invalid_github_url_exception import InvalidGitHubURLException
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.filters.tree_filter import TreeFilter
from src.integrations.git.github_repository_cloner import GitHubRepositoryCloner
from src.integrations.github_constants import GITHUB_URL_PREFIX, GITHUB_URL_PATTERN
from src.processors.pattern_set_processor import PatternSetProcessor
from src.strategies.ingest_strategy import IngestStrategy


class GitHubIngestStrategy(IngestStrategy):
    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            directory_scanner: WindowsDirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: WindowsFileReader,
            repository_cloner: GitHubRepositoryCloner,
    ):
        super().__init__(pattern_set_processor, tree_filter, directory_tree_renderer)
        self.directory_scanner = directory_scanner
        self.file_reader = file_reader
        self.repository_cloner = repository_cloner

    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith(GITHUB_URL_PREFIX)

    def _resolve_target(self, dto: IngestRequestDTO) -> Path:
        match = GITHUB_URL_PATTERN.match(dto.path.rstrip('/'))

        if match is None:
            raise InvalidGitHubURLException(dto.path)

        owner, repo = match.group('owner'), match.group('repo')

        url = f'https://github.com/{owner}/{repo}.git'

        return self.repository_cloner.clone(url)

    def _scan(self, target: Path) -> DirectoryNode:
        return self.directory_scanner.read(target)

    def _read_files(self, target: Path, directory_tree: DirectoryNode) -> str:
        return self.file_reader.read(directory_tree)
