class TokenEstimator:
    _CHARS_PER_TOKEN = 4

    def estimate(self, text: str) -> int:
        return len(text) // self._CHARS_PER_TOKEN

    @staticmethod
    def format(token_count: int) -> str:
        if token_count < 1000:
            return str(token_count)

        return f'{token_count / 1000:.1f}k'
