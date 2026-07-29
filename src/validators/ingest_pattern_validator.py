from src.dtos.pattern_dto import PatternDTO
from src.validators.pattern_rules.pattern_rule import PatternRule


class IngestPatternValidator:
    def __init__(self, *rules: PatternRule):
        self.rules = rules

    def validate(self, pattern: str) -> PatternDTO | None:
        for rule in self.rules:
            match = rule.match(pattern)

            if match is not None:
                return match

        return None
