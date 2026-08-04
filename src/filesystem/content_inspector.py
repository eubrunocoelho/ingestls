class ContentInspector:
    BINARY_CHECK_CHUNK_SIZE = 1024

    def is_binary(self, content: bytes) -> bool:
        return b'\x00' in content[:self.BINARY_CHECK_CHUNK_SIZE]

    @staticmethod
    def is_empty(content: bytes) -> bool:
        return len(content) == 0
