import base64

from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_http_client import GitHubHTTPClient


class GitHubBlobService:
    def __init__(self, http: GitHubHTTPClient):
        self.http = http

    def content(
            self,
            owner: str,
            repo: str,
            sha: str,
    ) -> bytes:
        payload = self.http.get(
            f'/repos/{owner}/{repo}/git/blobs/{sha}',
        )

        if payload.get('encoding') != 'base64':
            raise GitHubAPIException(
                f'Encoding inesperado ({payload.get("encoding")}) para o blob {sha}'
            )

        return base64.b64decode(payload['content'])
