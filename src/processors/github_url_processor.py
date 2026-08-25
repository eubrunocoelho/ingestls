from src.dtos.github_url_dto import GitHubURLDTO
from src.enums.github_url_type_enum import GitHubURLTypeEnum
from src.integrations.github_url_parser import GitHubURLParser
from src.integrations.github_ref_resolver import GitHubRefResolver


class GitHubURLProcessor:
    def __init__(
            self,
            parser: GitHubURLParser,
            ref_resolver: GitHubRefResolver
    ):
        self.parser = parser
        self.ref_resolver = ref_resolver

    def process(
            self,
            url: str
    ) -> GitHubURLDTO:
        parts = self.parser.parse(url)

        if not parts.segments:
            return self._build_repository_dto(parts)

        return self._build_reference_dto(parts)

    @staticmethod
    def _build_repository_dto(
            parts,
    ) -> GitHubURLDTO:
        return GitHubURLDTO(
            url=parts.url,
            owner=parts.owner,
            repository=parts.repository,
            type=GitHubURLTypeEnum.REPOSITORY,
            reference=None,
            path=None,
        )

    def _build_reference_dto(
            self,
            parts,
    ) -> GitHubURLDTO:
        url_type, reference, path = (
            self.ref_resolver.resolve(
                owner=parts.owner,
                repository=parts.repository,
                segments=parts.segments,
            )
        )

        return GitHubURLDTO(
            url=parts.url,
            owner=parts.owner,
            repository=parts.repository,
            type=url_type,
            reference=reference,
            path=path,
        )
