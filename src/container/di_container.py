from src.dispatchers.ingest_dispatcher import IngestDispatcher
from src.controllers.ingest_controller import IngestController
from src.rules.directory_exists_rule import DirectoryExistsRule
from src.services.ingest_service import IngestService
from src.validators.ingest_directory_validator import IngestDirectoryValidator
from src.strategies.windows_ingest_strategy import WindowsIngestStrategy

ingest_validator = IngestDirectoryValidator(
    DirectoryExistsRule(),
)

ingest_dispatcher = IngestDispatcher(
    WindowsIngestStrategy(),
)

ingest_service = IngestService(
    ingest_validator,
    ingest_dispatcher,
)

ingest_controller = IngestController(ingest_service)
