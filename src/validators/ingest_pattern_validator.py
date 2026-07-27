from src.enums.pattern_kind_enum import PatternKindEnum
from src.validators.pattern_rules.pattern_rule import PatternRule


class IngestPatternValidator:
    def __init__(self, *rules: PatternRule):
        self.rules = rules

    def validate(self, pattern: str) -> PatternKindEnum | None:
        for rule in self.rules:
            kind = rule.match(pattern)

            if kind is not None:
                return kind

        return None
