from typing import Mapping, Any

import requests

from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_constants import DEFAULT_TIMEOUT_SECONDS, GITHUB_API_BASE_URL


class GitHubHTTPClient:
    def __init__(
            self,
            token: str | None = None,
            timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ):
        self.token = token
        self.timeout = timeout

    def request(
            self,
            method: str,
            endpoint: str,
            params: Mapping[str, str] | None = None,
    ) -> requests.Response:
        try:
            return requests.request(
                method=method,
                url=f'{GITHUB_API_BASE_URL}{endpoint}',
                headers=self._headers(),
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise GitHubAPIException(
                f'Falha ao conectar com a API do GitHub: {error}'
            ) from error

    def get(self, endpoint: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        response = self.request(
            method='GET',
            endpoint=endpoint,
            params=params,
        )

        if response.status_code != 200:
            raise GitHubAPIException(
                f'Resposta inesperada da API do GitHub ({response.status_code}) '
                f'para {response.url}'
            )

        return response.json()

    def _headers(self) -> dict[str, str]:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
        }

        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        return headers
