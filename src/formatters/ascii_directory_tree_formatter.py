from src.models.directory_node import DirectoryNode


class AsciiDirectoryTreeFormatter:
    def format(self, root: DirectoryNode) -> str:
        lines = [
            'Directory structure:',
            f'└── {root.name}/',
        ]

        self._format_children(
            root.children,
            '',
            lines,
        )

        return '\n'.join(lines)

    def _format_children(
            self,
            children: list[DirectoryNode],
            prefix: str,
            lines: list[str],
    ) -> None:
        last = len(children) - 1

        for index, child in enumerate(children):
            connector = '└── ' if index == last else '├── '

            suffix = '/' if child.is_directory else ''

            lines.append(
                f'{prefix}{connector}{child.name}{suffix}'
            )

            if child.children:
                extension = '    ' if index == last else '│   '

                self._format_children(
                    child.children,
                    prefix + extension,
                    lines,
                )
