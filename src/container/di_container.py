from src.filesystem.directory_tree_renderer import DirectoryTreeRenderer
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner
from src.filesystem.windows_file_reader import WindowsFileReader
from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.controllers.ingest_controller import IngestController
from src.rules.directory_exists_rule import DirectoryExistsRule
from src.services.ingest_service import IngestService
from src.validators.ingest_directory_validator import IngestDirectoryValidator
from src.strategies.windows_ingest_strategy import WindowsIngestStrategy

windows_directory_scanner = WindowsDirectoryScanner()
windows_file_reader = WindowsFileReader()
directory_tree_renderer = DirectoryTreeRenderer()

windows_strategy = WindowsIngestStrategy(
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
