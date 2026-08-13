from src.config.paths import VIEWS_PATH
from src.integrations.github_ref_resolver import GitHubRefResolver
from src.integrations.github_repository_cloner import GitHubRepositoryCloner
from src.controllers.web_controller import WebController
from src.filesystem.content_inspector import ContentInspector
from src.filesystem.file_inspector import FileInspector
from src.filters.factories.locator_factory import LocatorFactory
from src.filters.factories.matcher_factory import MatcherFactory
from src.filters.tree_filter import TreeFilter
from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.controllers.ingest_controller import IngestController
from src.providers.view.jinja_view_provider import JinjaViewProvider
from src.services.ingest_service import IngestService
from src.strategies.github_ingest_strategy import GitHubIngestStrategy
from src.validators.directory_rules.directory_exists_rule import DirectoryExistsRule
from src.validators.directory_rules.github_url_format_rule import GitHubURLFormatRule
from src.validators.ingest_directory_validator import IngestDirectoryValidator
from src.strategies.windows_ingest_strategy import WindowsIngestStrategy
from src.processors.pattern_set_processor import PatternSetProcessor
from src.validators.ingest_pattern_validator import IngestPatternValidator
from src.validators.pattern_rules.extension_pattern_rule import ExtensionPatternRule
from src.validators.pattern_rules.filename_pattern_rule import FilenamePatternRule
from src.validators.pattern_rules.directory_pattern_rule import DirectoryPatternRule
from src.validators.pattern_rules.path_filename_pattern_rule import PathFilenamePatternRule
from src.validators.pattern_rules.recursive_directory_pattern_rule import RecursiveDirectoryPatternRule
from src.validators.pattern_rules.recursive_filename_pattern_rule import RecursiveFilenamePatternRule

# Web Dependencies
view_provider = JinjaViewProvider(
    views_path=VIEWS_PATH,
)

web_controller = WebController(
    view_provider,
)

# Ingest Dependencies
ingest_pattern_validator = IngestPatternValidator(
    ExtensionPatternRule(),
    FilenamePatternRule(),
    DirectoryPatternRule(),
    PathFilenamePatternRule(),
    RecursiveDirectoryPatternRule(),
    RecursiveFilenamePatternRule(),
)

pattern_set_processor = PatternSetProcessor(
    ingest_pattern_validator,
)

tree_filter = TreeFilter(
    LocatorFactory(),
    MatcherFactory()
)

content_inspector = ContentInspector()

file_inspector = FileInspector(
    content_inspector,
)

windows_file_reader = WindowsFileReader(
    file_inspector,
)

directory_tree_renderer = DirectoryTreeRenderer()

windows_ingest_strategy = WindowsIngestStrategy(
    pattern_set_processor,
    tree_filter,
    WindowsDirectoryScanner(),
    directory_tree_renderer,
    windows_file_reader,
)

github_ingest_strategy = GitHubIngestStrategy(
    pattern_set_processor,
    tree_filter,
    GitHubRepositoryCloner(),
    GitHubRefResolver(),
    WindowsDirectoryScanner(),
    directory_tree_renderer,
    windows_file_reader,
)

ingest_dispatcher = IngestDispatcher(
    windows_ingest_strategy,
    github_ingest_strategy,
)

ingest_directory_validator = IngestDirectoryValidator(
    DirectoryExistsRule(),
    GitHubURLFormatRule(),
)

ingest_service = IngestService(
    ingest_directory_validator,
    ingest_dispatcher,
)

ingest_controller = IngestController(ingest_service)
