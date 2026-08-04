from typing import Any

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.github.invalid_github_url_exception import InvalidGitHubURLException
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.github_directory_scanner import GitHubDirectoryScanner
from src.filesystem.github_file_reader import GitHubFileReader
from src.filters.tree_filter import TreeFilter
from src.integrations.github_constants import GITHUB_URL_PREFIX, GITHUB_URL_PATTERN
from src.processors.pattern_set_processor import PatternSetProcessor
from src.strategies.ingest_strategy import IngestStrategy


class GitHubIngestStrategy(IngestStrategy):
    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            directory_scanner: GitHubDirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: GitHubFileReader,
    ):
        super().__init__(pattern_set_processor, tree_filter, directory_tree_renderer)
        self.directory_scanner = directory_scanner
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith(GITHUB_URL_PREFIX)

    def _resolve_target(self, dto: IngestRequestDTO) -> tuple[str, str]:
        match = GITHUB_URL_PATTERN.match(dto.path.rstrip('/'))

        if match is None:
            raise InvalidGitHubURLException(dto.path)

        return match.group('owner'), match.group('repo')

    def _scan(self, target: tuple[str, str]) -> DirectoryNode:
        owner, repo = target

        return self.directory_scanner.read(owner, repo)

    def _read_files(self, target: Any, directory_tree: DirectoryNode) -> str:
        owner, repo = target

        return self.file_reader.read(directory_tree, owner, repo)
