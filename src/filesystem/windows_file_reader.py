from pathlib import Path

from src.filesystem.file_reader import FileReader

FILE_INFO = (
    '================================================\n'
    'FILE: {filename}\n'
    'DIRECTORY: {directory}\n'
    '================================================'
)


class WindowsFileReader(FileReader):
    def read(self, root: Path) -> str:
        contents = []

        for file in root.rglob('*'):
            if file.is_file():
                contents.append(FILE_INFO.format(
                    filename=file.name,
                    directory=file.parent.relative_to(root),
                ))

                contents.append(
                    file.read_text(
                        encoding='utf-8',
                    )
                )

        return '\n'.join(contents)
