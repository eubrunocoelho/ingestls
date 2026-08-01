from pathlib import Path


class FileInspector:
    _BINARY_CHECK_CHUNK_SIZE = 1024

    def is_binary(self, file_path: Path) -> bool:
        try:
            with open(file_path, 'rb') as handle:
                return b'\x00' in handle.read(self._BINARY_CHECK_CHUNK_SIZE)
        except OSError:
            return True

    @staticmethod
    def is_empty(file_path: Path) -> bool:
        try:
            return file_path.stat().st_size == 0
        except OSError:
            return False
