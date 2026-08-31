from pathlib import Path
import logging

from src.dtos.file_read_result_dto import FileReadResultDTO
from src.providers.ingest_summary_provider import IngestSummaryProvider
from src.dtos.github_url_dto import GitHubURLDTO
from src.dtos.ingest_request_dto import IngestRequestDTO
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.filters.tree_filter import TreeFilter
from src.integrations.github_repository_cloner import GitHubRepositoryCloner
from src.integrations.github_url import GITHUB_URL_PREFIX
from src.processors.github_url_processor import GitHubURLProcessor
from src.processors.pattern_set_processor import PatternSetProcessor
from src.strategies.ingest_strategy import IngestStrategy

logger = logging.getLogger(__name__)


class GitHubIngestStrategy(IngestStrategy[tuple[GitHubURLDTO, Path]]):
    _GIT_DIR_NAME = '.git'

    def __init__(
            self,
            pattern_set_processor: PatternSetProcessor,
            tree_filter: TreeFilter,
            url_processor: GitHubURLProcessor,
            repository_cloner: GitHubRepositoryCloner,
            directory_scanner: WindowsDirectoryScanner,
            directory_tree_renderer: DirectoryTreeRenderer,
            file_reader: WindowsFileReader,
            ingest_summary_provider: IngestSummaryProvider,

    ):
        super().__init__(
            pattern_set_processor,
            tree_filter,
            directory_tree_renderer,
            ingest_summary_provider
        )

        self.url_processor = url_processor
        self.repository_cloner = repository_cloner
        self.directory_scanner = directory_scanner
        self.file_reader = file_reader

    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith(GITHUB_URL_PREFIX)

    def _resolve_target(self, dto: IngestRequestDTO) -> tuple[GitHubURLDTO, Path]:
        url_dto = self.url_processor.process(dto.path)

        clone_url = (
            f'{GITHUB_URL_PREFIX}'
            f'{url_dto.owner}/'
            f'{url_dto.repository}'
        )

        local_path = self.repository_cloner.clone(
            url=clone_url,
            ref=url_dto.reference,
            ref_type=url_dto.type,
        )

        return url_dto, local_path

    def _scan(
            self,
            target: tuple[GitHubURLDTO, Path]
    ) -> DirectoryNode:
        url_dto, local_path = target

        directory_tree = self.directory_scanner.read(
            local_path
        )

        directory_tree.name = url_dto.repository

        directory_tree.children = [
            child
            for child in directory_tree.children
            if child.name != self._GIT_DIR_NAME
        ]

        if url_dto.path:
            directory_tree = self._narrow_to_path(
                directory_tree,
                url_dto.path
            )

        return directory_tree

    def _read_files(
            self,
            target: tuple[GitHubURLDTO, Path],
            directory_tree: DirectoryNode
    ) -> FileReadResultDTO:
        return self.file_reader.read(directory_tree)

    def _describe_target(self, target: tuple[GitHubURLDTO, Path]) -> str:
        url_dto, _ = target

        return (
            f'{url_dto.owner}/'
            f'{url_dto.repository}'
        )

    def _describe_reference(
            self,
            target: tuple[GitHubURLDTO, Path],
    ) -> str | None:
        url_dto, _ = target

        if url_dto.reference is None:
            return None

        return (
            f'{url_dto.type.value} '
            f'{url_dto.reference}'
        )

    def _cleanup(self, target: tuple[GitHubURLDTO, Path]) -> None:
        _, local_path = target

        try:
            self.repository_cloner.cleanup(
                local_path
            )

        except Exception:
            logger.warning(
                'Falha ao limpar diretório temporário %s (será removido depois).',
                local_path,
                exc_info=True
            )

    @staticmethod
    def _narrow_to_path(
            root: DirectoryNode,
            path: str
    ) -> DirectoryNode:
        node = root

        for segment in path.split('/'):
            match = next(
                (
                    child for child in node.children
                    if child.name == segment
                ),
                None
            )

            if match is None or not match.is_directory:
                raise ValueError(
                    f'Caminho não encontrado no repositório: {path}'
                )

            node = match

        return node
