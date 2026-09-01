from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_stats import DirectoryTreeStats
from src.providers.token_estimator import TokenEstimator


class IngestSummaryProvider:
    def __init__(self, token_estimator: TokenEstimator):
        self.token_estimator = token_estimator

    def build(
            self,
            target_label: str,
            directory_tree: DirectoryNode,
            directory_structure: str,
            files_content: str,
            code_line_count: int,
            github_reference: str | None = None,
    ) -> str:
        stats = DirectoryTreeStats.from_tree(directory_tree)

        token_count = self.token_estimator.estimate(directory_structure + files_content)

        lines = [
            f'Repositório/Diretório: {target_label}',
        ]

        if github_reference is not None:
            lines.append(
                f'Referência do GitHub: {github_reference}',
            )

        lines.append(
            f'Diretórios: {stats.directory_count}',
        )

        lines.append(
            f'Arquivos Analisados: {stats.file_count}',
        )

        lines.append(
            f'Linhas de Código: '
            f'{self._format_thousands(code_line_count)}',
        )

        lines.append('')

        lines.append(
            f'Estimativa de Tokens: '
            f'{self.token_estimator.format(token_count)}',
        )

        return '\n'.join(lines)

    @staticmethod
    def _format_thousands(value: int) -> str:
        return f'{value:,}'.replace(',', '.')
