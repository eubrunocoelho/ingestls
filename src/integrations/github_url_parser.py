from urllib.parse import urlparse

from src.dtos.github_url_parts_dto import GitHubURLPartsDTO
from src.exceptions.github.invalid_github_url_exception import InvalidGitHubURLException


class GitHubURLParser:
    @staticmethod
    def parse(url: str) -> GitHubURLPartsDTO:
        parsed = urlparse(url)

        if parsed.scheme != 'https':
            raise InvalidGitHubURLException(
                'A URL do GitHub deve utilizar HTTPS.'
            )

        if parsed.netloc.lower() != 'github.com':
            raise InvalidGitHubURLException(
                'A URL deve pertencer ao domínio github.com.'
            )

        segments = tuple(
            segment
            for segment in parsed.path.split('/')
            if segment
        )

        if len(segments) < 2:
            raise InvalidGitHubURLException(
                'A URL deve possuir owner e repository.'
            )

        owner = segments[0]
        repository = segments[1]

        if repository.endswith('.git'):
            repository = repository[:-4]

        if not owner or not repository:
            raise InvalidGitHubURLException(
                'Owner e repository são obrigatórios.'
            )

        # https://github.com/owner/repository
        if len(segments) == 2:
            return GitHubURLPartsDTO(
                url=url,
                owner=owner,
                repository=repository,
                segments=(),
            )

        # Tudo depois de `/tree/` será resolvido pelo `GitHubRefResolver`
        if segments[2] != 'tree':
            raise InvalidGitHubURLException(
                'A URL do GitHub deve utilizar /tree/.'
            )

        if len(segments) < 4:
            raise InvalidGitHubURLException(
                'A URL /tree/ deve possuir uma referência.'
            )

        return GitHubURLPartsDTO(
            url=url,
            owner=owner,
            repository=repository,
            segments=segments[3:]
        )
