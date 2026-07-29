from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.controllers.ingest_controller import IngestController
from src.services.ingest_service import IngestService
from src.validators.directory_rules.directory_exists_rule import DirectoryExistsRule
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

windows_directory_scanner = WindowsDirectoryScanner()

windows_file_reader = WindowsFileReader()

directory_tree_renderer = DirectoryTreeRenderer()

windows_strategy = WindowsIngestStrategy(
    pattern_set_processor,
    windows_directory_scanner,
    directory_tree_renderer,
    windows_file_reader,
)

ingest_dispatcher = IngestDispatcher(
    windows_strategy,
)

ingest_validator = IngestDirectoryValidator(
    DirectoryExistsRule(),
)

ingest_service = IngestService(
    ingest_validator,
    ingest_dispatcher,
)

ingest_controller = IngestController(ingest_service)
