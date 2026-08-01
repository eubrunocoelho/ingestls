from pathlib import Path

from src.filesystem.directory_node import DirectoryNode
from src.filesystem.file_inspector import FileInspector
from src.filesystem.file_reader import FileReader


class WindowsFileReader(FileReader):
    _FILE_INFO = (
        '================================================\n'
        'FILE: {filename}\n'
        'DIRECTORY: {directory}\n'
        '================================================'
    )

    _BINARY_FILE_FLAG = '[Binary File]'
    _EMPTY_FILE_FLAG = '[Empty File]'

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
            directory = file_path.parent.relative_to(root_path)
            directory_display = './' if str(directory) == '.' else str(directory)

            contents.append(self._FILE_INFO.format(
                filename=child.name,
                directory=directory_display,
            ))

            contents.append(self._get_file_content(file_path))

    def _get_file_content(self, file_path: Path) -> str:
        if self.file_inspector.is_empty(file_path):
            return self._EMPTY_FILE_FLAG

        if self.file_inspector.is_binary(file_path):
            return self._BINARY_FILE_FLAG

        return file_path.read_text(encoding='utf-8')
