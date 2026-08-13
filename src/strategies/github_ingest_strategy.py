from pathlib import Path

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.exceptions.github.invalid_github_url_exception import InvalidGitHubURLException
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.filters.tree_filter import TreeFilter
from src.integrations.github_ref_resolver import GitHubRefResolver
from src.integrations.github_repository_cloner import GitHubRepositoryCloner
from src.integrations.github_constants import GITHUB_URL_PREFIX, GITHUB_URL_PATTERN
from src.processors.pattern_set_processor import PatternSetProcessor
from src.strategies.ingest_strategy import IngestStrategy

_GIT_DIR_NAME = '.git'


class GitHubIngestStrategy(IngestStrategy):
    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            repository_cloner: GitHubRepositoryCloner,
            ref_resolver: GitHubRefResolver,
            directory_scanner: WindowsDirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: WindowsFileReader,

    ):
        super().__init__(pattern_set_processor, tree_filter, directory_tree_renderer)
        self.repository_cloner = repository_cloner
        self.ref_resolver = ref_resolver
        self.directory_scanner = directory_scanner
        self.file_reader = file_reader

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
        directory_tree = self.directory_scanner.read(target)
        directory_tree.children = [
            child for child in directory_tree.children if child.name != _GIT_DIR_NAME
        ]

        return directory_tree

    def _read_files(self, target: Path, directory_tree: DirectoryNode) -> str:
        return self.file_reader.read(directory_tree)

    def _cleanup(self, target: Path) -> None:
        self.repository_cloner.cleanup(target)
