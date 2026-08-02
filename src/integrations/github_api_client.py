import requests
import base64

from src.dtos.github_tree_item_dto import GitHubTreeItemDTO
from src.exceptions.github_api_exception import GitHubAPIException
from src.integrations.github_client import GitHubClient

GITHUB_API_BASE_URL = 'https://api.github.com'
DEFAULT_TIMEOUT_SECONDS = 10.0


class GitHubAPIClient(GitHubClient):
    def __init__(self, token: str | None = None, timeout: float = DEFAULT_TIMEOUT_SECONDS):
        self.token = token
        self.timeout = timeout

    def repository_exists(self, owner: str, repo: str) -> bool:
        try:
            response = requests.get(
                f'{GITHUB_API_BASE_URL}/repos/{owner}/{repo}',
                headers=self._headers(),
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise GitHubAPIException(
                f'Falha ao conectar com a API do GitHub: {error}'
            ) from error

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise GitHubAPIException(
            f'Resposta inesperada da API do GitHub ({response.status_code}) '
            f'para {owner}/{repo}'
        )

    def get_default_branch(self, owner: str, repo: str) -> str:
        response = self._get(f'{GITHUB_API_BASE_URL}/repos/{owner}/{repo}')

        return response.json()['default_branch']

    def get_repository_tree(self, owner: str, repo: str, branch: str) -> list[GitHubTreeItemDTO]:
        response = self._get(
            f'{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/git/trees/{branch}',
            params={'recursive': '1'},
        )

        payload = response.json()

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

    def get_blob_content(self, owner: str, repo: str, sha: str) -> bytes:
        response = self._get(f'{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/git/blobs/{sha}')
        payload = response.json()

        if payload.get('encoding') != 'base64':
            raise GitHubAPIException(
                f'Encoding inesperado ({payload.get("encoding")}) para o blob {sha}'
            )

        return base64.b64decode(payload['content'])

    def _get(self, url: str, params: dict | None = None) -> requests.Response:
        try:
            response = requests.get(
                url,
                headers=self._headers(),
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise GitHubAPIException(
                f'Falha ao conectar com a API do GitHub: {error}'
            ) from error

        if response.status_code != 200:
            raise GitHubAPIException(
                f'Resposta inesperada da API do GitHub ({response.status_code}) '
                f'para {url}'
            )

        return response

    def _headers(self) -> dict[str, str]:
        headers = {'Accept': 'application/vnd.github.v3+json'}

        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        return headers
