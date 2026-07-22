from src.dtos.ingest_request import IngestRequest
from src.rules.ingest_rule import IngestRule


class IngestDirectoryValidator:
    def __init__(self, *rules: IngestRule):
        self.rules = rules

    def validate(self, dto: IngestRequest) -> None:
        for rule in self.rules:
            rule.validate(dto)
