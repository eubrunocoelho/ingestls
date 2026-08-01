import requests

from src.exceptions.github_api_exception import GitHubApiException
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
                # Unresolved attribute reference '_headers' for class 'GitHubAPIClient'
                headers=self._headers(),
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise GitHubApiException(
                f'Falha ao conectar com a API do GitHub: {error}'
            ) from error

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise GitHubApiException(
            f'Resposta inesperada da API do GitHub ({response.status_code}) '
            f'para {owner}/{repo}'
        )

    def _headers(self) -> dict[str, str]:
        headers = {'Accept': 'application/vnd.github.v3+json'}

        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        return headers
