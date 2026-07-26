from src.filesystem.directory_node import DirectoryNode


class DirectoryTreeRenderer:
    def render_tree(self, root: DirectoryNode) -> str:
        lines = [
            'Estrutura de diretório:',
            f'└── {root.name}/',
        ]

        self._dfs(
            node=root,
            prefix='    ',
            lines=lines,
        )

        return '\n'.join(lines)

    def _dfs(
            self,
            node: DirectoryNode,
            prefix: str,
            lines: list[str],
    ) -> None:
        total = len(node.children)

        for index, child in enumerate(node.children):
            last = index == total - 1

            connector = '└── ' if last else '├── '
            suffix = '/' if child.is_directory else ''

            lines.append(
                f'{prefix}{connector}{child.name}{suffix}'
            )

            if child.is_directory:
                next_prefix = prefix + ('    ' if last else '│   ')
                self._dfs(
                    node=child,
                    prefix=next_prefix,
                    lines=lines,
                )
