class ContentInspector:
    @staticmethod
    def is_binary(content: bytes) -> bool:
        if not content:
            return False

        if b'\x00' in content:
            return True

        non_text = sum(
            byte < 32 and byte not in (9, 10, 13)
            for byte in content
        )

        return non_text / len(content) > 0.30
