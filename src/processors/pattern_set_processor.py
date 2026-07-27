from src.dtos.pattern_dto import PatternDTO
from src.validators.ingest_pattern_validator import IngestPatternValidator


class PatternSetProcessor:
    def __init__(self, validator: IngestPatternValidator):
        self.validator = validator

    def process(self, pattern: str | None) -> list[PatternDTO]:
        if not pattern:
            return []

        result: list[PatternDTO] = []

        for item in pattern.split(','):
            item = item.strip()

            if not item:
                continue

            kind = self.validator.validate(item)

            if kind is None:
                continue

            result.append(
                PatternDTO(
                    pattern=item,
                    kind=kind,
                )
            )

        return result
