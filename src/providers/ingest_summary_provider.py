from src.filesystem.directory_node import DirectoryNode
from src.filesystem.directory_tree_stats import DirectoryTreeStats
from src.providers.token_estimator import TokenEstimator

_SUMMARY_TEMPLATE = (
    'Repositório/Diretório: {target_label}\n'
    'Diretórios: {directory_count}\n'
    'Arquivos Analisados: {file_count}\n'
    '\n'
    'Estimativa de Tokens: {token_estimate}'
)


class IngestSummaryProvider:
    def __init__(self, token_estimator: TokenEstimator):
        self.token_estimator = token_estimator

    def build(self, target_label: str, directory_tree: DirectoryNode, directory_structure: str,
              files_content: str) -> str:
        stats = DirectoryTreeStats.from_tree(directory_tree)
        token_count = self.token_estimator.estimate(directory_structure + files_content)

        return _SUMMARY_TEMPLATE.format(
            target_label=target_label,
            directory_count=stats.directory_count,
            file_count=stats.file_count,
            token_estimate=self.token_estimator.format(token_count)
        )
