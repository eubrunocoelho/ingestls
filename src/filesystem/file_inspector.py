from pathlib import Path

from src.filesystem.content_inspector import ContentInspector


class FileInspector:
    def __init__(self, content_inspector: ContentInspector):
        self.content_inspector = content_inspector

    def is_binary(self, file_path: Path) -> bool:
        try:
            with open(file_path, 'rb') as handle:
                chunk = handle.read(self.content_inspector.BINARY_CHECK_CHUNK_SIZE)
        except OSError:
            return True

        return self.content_inspector.is_binary(chunk)

    @staticmethod
    def is_empty(file_path: Path) -> bool:
        try:
            return file_path.stat().st_size == 0
        except OSError:
            return False
