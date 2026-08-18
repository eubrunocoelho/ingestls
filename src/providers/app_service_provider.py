from src.providers.ingest_summary_provider import IngestSummaryProvider
from src.providers.token_estimator import TokenEstimator
from src.config.paths import VIEWS_PATH, TMP_DIR
from src.container.di_container import DIContainer
from src.controllers.ingest_controller import IngestController
from src.controllers.web_controller import WebController
from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.filesystem.content_inspector import ContentInspector
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.file_inspector import FileInspector
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.filters.factories.locator_factory import LocatorFactory
from src.filters.factories.matcher_factory import MatcherFactory
from src.filters.tree_filter import TreeFilter
from src.github.parsers.github_url_parser import GitHubURLParser
from src.github.resolvers.github_ref_resolver import GitHubRefResolver
from src.integrations.github_repository_cloner import GitHubRepositoryCloner
from src.processors.github_url_processor import GitHubURLProcessor
from src.processors.pattern_set_processor import PatternSetProcessor
from src.providers.jinja_view_provider import JinjaViewProvider
from src.services.ingest_service import IngestService
from src.strategies.github_ingest_strategy import GitHubIngestStrategy
from src.strategies.windows_ingest_strategy import WindowsIngestStrategy
from src.validators.directory_rules.directory_exists_rule import DirectoryExistsRule
from src.validators.directory_rules.github_url_format_rule import GitHubURLFormatRule
from src.validators.ingest_directory_validator import IngestDirectoryValidator
from src.validators.ingest_pattern_validator import IngestPatternValidator
from src.validators.pattern_rules.directory_pattern_rule import DirectoryPatternRule
from src.validators.pattern_rules.extension_pattern_rule import ExtensionPatternRule
from src.validators.pattern_rules.filename_pattern_rule import FilenamePatternRule
from src.validators.pattern_rules.path_filename_pattern_rule import PathFilenamePatternRule
from src.validators.pattern_rules.recursive_directory_pattern_rule import RecursiveDirectoryPatternRule
from src.validators.pattern_rules.recursive_filename_pattern_rule import RecursiveFilenamePatternRule


class AppServiceProvider:
    def register(self, container: DIContainer) -> None:
        self._register_web(container)
        self._register_filesystem(container)
        self._register_filters(container)
        self._register_github(container)
        self._register_summary(container)
        self._register_ingest(container)

    @staticmethod
    def _register_web(container: DIContainer) -> None:
        container.singleton(
            JinjaViewProvider,
            lambda: JinjaViewProvider(
                views_path=VIEWS_PATH
            )
        )

        container.singleton(
            WebController,
            lambda: WebController(
                container.resolve(JinjaViewProvider),
            )
        )

    @staticmethod
    def _register_filesystem(container: DIContainer) -> None:
        container.singleton(
            ContentInspector,
            lambda: ContentInspector(),
        )

        container.singleton(
            FileInspector,
            lambda: FileInspector(
                container.resolve(ContentInspector)
            )
        )

        container.singleton(
            WindowsFileReader,
            lambda: WindowsFileReader(
                container.resolve(FileInspector),
            )
        )

        container.singleton(
            WindowsDirectoryScanner,
            lambda: WindowsDirectoryScanner(),
        )

        container.singleton(
            DirectoryTreeRenderer,
            lambda: DirectoryTreeRenderer()
        )

    @staticmethod
    def _register_filters(container: DIContainer) -> None:
        container.singleton(
            LocatorFactory,
            lambda: LocatorFactory()
        )

        container.singleton(
            MatcherFactory,
            lambda: MatcherFactory()
        )

        container.singleton(
            TreeFilter,
            lambda: TreeFilter(
                container.resolve(LocatorFactory),
                container.resolve(MatcherFactory),
            )
        )

    @staticmethod
    def _register_github(container: DIContainer) -> None:
        container.singleton(
            GitHubURLParser,
            lambda: GitHubURLParser()
        )

        container.singleton(
            GitHubRefResolver,
            lambda: GitHubRefResolver(),
        )

        container.singleton(
            GitHubURLProcessor,
            lambda: GitHubURLProcessor(
                container.resolve(GitHubURLParser),
                container.resolve(GitHubRefResolver)
            )
        )

        container.singleton(
            GitHubRepositoryCloner,
            lambda: GitHubRepositoryCloner(
                TMP_DIR
            )
        )

    @staticmethod
    def _register_summary(container: DIContainer) -> None:
        container.singleton(
            TokenEstimator,
            lambda: TokenEstimator()
        )

        container.singleton(
            IngestSummaryProvider,
            lambda: IngestSummaryProvider(
                container.resolve(TokenEstimator)
            )
        )

    @staticmethod
    def _register_ingest(container: DIContainer) -> None:
        container.singleton(
            IngestPatternValidator,
            lambda: IngestPatternValidator(
                ExtensionPatternRule(),
                FilenamePatternRule(),
                DirectoryPatternRule(),
                PathFilenamePatternRule(),
                RecursiveDirectoryPatternRule(),
                RecursiveFilenamePatternRule(),
            )
        )

        container.singleton(
            PatternSetProcessor,
            lambda: PatternSetProcessor(
                container.resolve(IngestPatternValidator)
            )
        )

        container.singleton(
            WindowsIngestStrategy,
            lambda: WindowsIngestStrategy(
                container.resolve(PatternSetProcessor),
                container.resolve(TreeFilter),
                container.resolve(WindowsDirectoryScanner),
                container.resolve(DirectoryTreeRenderer),
                container.resolve(WindowsFileReader),
                container.resolve(IngestSummaryProvider)
            )
        )

        container.singleton(
            GitHubIngestStrategy,
            lambda: GitHubIngestStrategy(
                container.resolve(PatternSetProcessor),
                container.resolve(TreeFilter),
                container.resolve(GitHubURLProcessor),
                container.resolve(GitHubRepositoryCloner),
                container.resolve(WindowsDirectoryScanner),
                container.resolve(DirectoryTreeRenderer),
                container.resolve(WindowsFileReader),
                container.resolve(IngestSummaryProvider)
            )
        )

        container.singleton(
            IngestDispatcher,
            lambda: IngestDispatcher(
                container.resolve(WindowsIngestStrategy),
                container.resolve(GitHubIngestStrategy),
            )
        )

        container.singleton(
            IngestDirectoryValidator,
            lambda: IngestDirectoryValidator(
                DirectoryExistsRule(),
                GitHubURLFormatRule(),
            )
        )

        container.singleton(
            IngestService,
            lambda: IngestService(
                container.resolve(IngestDirectoryValidator),
                container.resolve(IngestDispatcher),
            )
        )

        container.singleton(
            IngestController,
            lambda: IngestController(
                container.resolve(IngestService)
            )
        )
