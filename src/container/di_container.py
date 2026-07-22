from src.readers.windows_directory_reader import WindowsDirectoryReader
from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.controllers.ingest_controller import IngestController
from src.rules.directory_exists_rule import DirectoryExistsRule
from src.services.ingest_service import IngestService
from src.validators.ingest_directory_validator import IngestDirectoryValidator
from src.strategies.windows_ingest_strategy import WindowsIngestStrategy

windows_reader = WindowsDirectoryReader()

windows_strategy = WindowsIngestStrategy(
    windows_reader,
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
