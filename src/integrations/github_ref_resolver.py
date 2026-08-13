import re

from dulwich import porcelain

from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_constants import GITHUB_URL_PREFIX

_SHA_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')


class GitHubRefResolver:
    def resolve(
            self,
            owner: str,
            repo: str,
            segments: tuple[str, ...],
    ) -> tuple[str, str | None]:
        if not segments:
            raise GitHubAPIException('Nenhuma referência informada.')

        if _SHA_PATTERN.fullmatch(segments[0]):
            path = '/'.join(segments[1:]) or None
            return segments[0], path

        url = f'{GITHUB_URL_PREFIX}{owner}/{repo}'

        try:
            refs = porcelain.ls_remote(url)
        except Exception as error:
            raise GitHubAPIException(
                f'Falha ao listar referências de {owner}/{repo}: {error}'
            ) from error

        ref_names = {
            name.decode().removeprefix('refs/heads/').removeprefix('refs/tags/')
            for name in refs
            if name.startswith(b'refs/heads/') or name.startswith(b'refs/tags/')
        }

        for index in range(len(segments), 0, -1):
            candidate = '/'.join(segments[:index])

            if candidate in ref_names:
                path = '/'.join(segments[index:]) or None
                return candidate, path

        raise GitHubAPIException(
            f'Referência não encontrada em {owner}/{repo}: {segments[0]}'
        )
