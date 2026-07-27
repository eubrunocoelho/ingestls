class PatternSetProcessor:
    @staticmethod
    def process(pattern: str|None) -> list[str]:
        if not pattern:
            return []

        return [
            pattern.strip()
            for pattern in pattern.split(',')
            if pattern.strip()
        ]
