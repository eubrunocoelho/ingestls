from src.controllers.ingest_controller import IngestController
from src.rules.directory_exists_rule import DirectoryExistsRule
from src.services.ingest_service import IngestService
from src.validators.ingest_directory_validator import IngestDirectoryValidator

validator = IngestDirectoryValidator(
    DirectoryExistsRule(),
)

ingest_service = IngestService(validator)

ingest_controller = IngestController(ingest_service)
