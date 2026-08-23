import re

from dulwich import porcelain
from src.enums.github_url_type_enum import GitHubURLTypeEnum
from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_constants import GITHUB_URL_PREFIX

_SHA_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')


class GitHubRefResolver:
    def resolve(
            self,
            owner: str,
            repository: str,
            segments: tuple[str, ...]
    ) -> tuple[GitHubURLTypeEnum, str, str | None]:
        if not segments:
            raise GitHubAPIException('Nenhuma referência informada.')

        if _SHA_PATTERN.fullmatch(segments[0]):
            return GitHubURLTypeEnum.COMMIT, segments[0], self._make_path(segments[1:])

        url = f'{GITHUB_URL_PREFIX}{owner}/{repository}'

        try:
            refs = porcelain.ls_remote(url).refs
        except Exception as error:
            raise GitHubAPIException(
                f'Falha ao listar referências de {owner}/{repository}: {error}'
            ) from error

        branches = self._ref_names(refs, b'refs/heads/')
        tags = self._ref_names(refs, b'refs/tags/')

        for index in range(len(segments), 0, -1):
            candidate = '/'.join(segments[:index])
            path = self._make_path(segments[index:])

            if candidate in branches:
                return GitHubURLTypeEnum.BRANCH, candidate, path

            if candidate in tags:
                return GitHubURLTypeEnum.TAG, candidate, path

        raise GitHubAPIException(
            f'Referência não encontrada em {owner}/{repository}: {segments[0]}'
        )

    @staticmethod
    def _ref_names(refs: dict, prefix: bytes) -> set[str]:
        return {
            name.decode().removeprefix(prefix.decode())
            for name in refs
            if name.startswith(prefix)
        }

    @staticmethod
    def _make_path(segments: tuple[str, ...]) -> str | None:
        return '/'.join(segments) if segments else None
