from pathlib import Path

from src.filesystem.directory_node import DirectoryNode
from src.filesystem.file_inspector import FileInspector
from src.filesystem.ingest_format import EMPTY_FILE_FLAG, BINARY_FILE_FLAG, FILE_START, FILE_END


class WindowsFileReader:
    def __init__(self, file_inspector: FileInspector):
        self.file_inspector = file_inspector

    def read(self, tree: DirectoryNode) -> str:
        contents: list[str] = []
        root_path = Path(tree.path)

        self._collect(tree, root_path, contents)

        return '\n'.join(contents)

    def _collect(
            self,
            node: DirectoryNode,
            root_path: Path,
            contents: list[str],
    ) -> None:
        for child in node.children:
            if child.is_directory:
                self._collect(child, root_path, contents)

                continue

            file_path = Path(child.path)
            relative_path = file_path.relative_to(root_path)

            contents.append(
                FILE_START.format(
                    path=relative_path.as_posix(),
                )
            )

            contents.append(
                self._get_file_content(file_path)
            )

            contents.append(FILE_END)

    def _get_file_content(self, file_path: Path) -> str:
        if self.file_inspector.is_empty(file_path):
            return EMPTY_FILE_FLAG

        if self.file_inspector.is_binary(file_path):
            return BINARY_FILE_FLAG

        return file_path.read_text(encoding='utf-8')
