from src.dtos.ingest_request_dto import IngestRequestDTO
from src.validators.directory_rules.ingest_rule import IngestRule


class IngestDirectoryValidator:
    def __init__(self, *rules: IngestRule):
        self.rules = rules

    def validate(self, dto: IngestRequestDTO) -> None:
        for rule in self.rules:
            rule.validate(dto)
