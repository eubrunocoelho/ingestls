from pathlib import Path

from src.filesystem.content_inspector import ContentInspector


class FileInspector:
    _BINARY_CHECK_CHUNK_SIZE = 8192

    def __init__(self, content_inspector: ContentInspector):
        self.content_inspector = content_inspector

    def is_binary(self, file_path: Path) -> bool:
        try:
            with file_path.open('rb') as handle:
                content = handle.read(self._BINARY_CHECK_CHUNK_SIZE)
        except OSError:
            return True

        return self.content_inspector.is_binary(content)
