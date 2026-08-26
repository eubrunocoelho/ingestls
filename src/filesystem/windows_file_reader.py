from pathlib import Path

from src.dtos.file_read_result_dto import FileReadResultDTO
from src.filesystem.directory_node import DirectoryNode
from src.filesystem.file_inspector import FileInspector
from src.filesystem.file_output_format import EMPTY_FILE_FLAG, BINARY_FILE_FLAG, FILE_START, FILE_END


class WindowsFileReader:
    def __init__(self, file_inspector: FileInspector):
        self.file_inspector = file_inspector

    def read(self, tree: DirectoryNode) -> FileReadResultDTO:
        contents: list[str] = []
        line_counts: list[int] = []

        root_path = Path(tree.path)

        self._collect(tree, root_path, contents, line_counts)

        return FileReadResultDTO(
            content='\n'.join(contents),
            code_line_count=sum(line_counts)
        )

    def _collect(
            self,
            node: DirectoryNode,
            root_path: Path,
            contents: list[str],
            line_counts: list[int]
    ) -> None:
        for child in node.children:
            if child.is_directory:
                self._collect(child, root_path, contents, line_counts)
                continue

            file_path = Path(child.path)
            relative_path = file_path.relative_to(root_path)

            contents.append(
                FILE_START.format(
                    path=relative_path.as_posix(),
                )
            )

            file_content = self._get_file_content(file_path)

            contents.append(file_content)

            line_counts.append(self._count_code_lines(file_content))

            contents.append(FILE_END)

    def _get_file_content(self, file_path: Path) -> str:
        if self.file_inspector.is_binary(file_path):
            return BINARY_FILE_FLAG

        if file_path.stat().st_size == 0:
            return EMPTY_FILE_FLAG

        return file_path.read_text(encoding='utf-8')

    @staticmethod
    def _count_code_lines(content: str) -> int:
        if content in (BINARY_FILE_FLAG, EMPTY_FILE_FLAG):
            return 0

        return content.count('\n') + 1
