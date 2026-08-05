from src.dtos.github_tree_item_dto import GitHubTreeItemDTO
from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_http_client import GitHubHTTPClient


class GitHubRepositoryService:
    def __init__(self, http: GitHubHTTPClient):
        self.http = http

    def exists(self, owner: str, repo: str) -> bool:
        response = self.http.request(
            method='GET',
            endpoint=f'/repos/{owner}/{repo}',
        )

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise GitHubAPIException(
            f'Resposta inesperada da API do GitHub ({response.status_code}) '
            f'para {owner}/{repo}'
        )

    def default_branch(self, owner: str, repo: str) -> str:
        payload = self.http.get(f'/repos/{owner}/{repo}')

        return payload['default_branch']

    def tree(
            self,
            owner: str,
            repo: str,
            branch: str,
    ) -> list[GitHubTreeItemDTO]:
        payload = self.http.get(
            f'/repos/{owner}/{repo}/git/trees/{branch}',
            params={'recursive': '1'}
        )

        if payload.get('truncated'):
            raise GitHubAPIException(
                f'A árvore de {owner}/{repo}@{branch} foi truncada pela API do '
                f'GitHub (repositório muito grande). Paginação ainda não suportada.'
            )

        return [
            GitHubTreeItemDTO(
                path=item['path'],
                type=item['type'],
                sha=item['sha'],
                size=item.get('size'),
            )
            for item in payload.get('tree', [])
            if item['type'] in ('blob', 'tree')
        ]
