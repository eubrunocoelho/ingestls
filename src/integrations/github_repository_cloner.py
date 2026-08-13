import shutil
import tempfile
from pathlib import Path

from dulwich import porcelain

from src.exceptions.github.github_api_exception import GitHubAPIException


class GitHubRepositoryCloner:
    def __init__(self, depth: int = 1):
        self.depth = depth

    def clone(self, url: str, ref: str | None = None) -> Path:
        target = Path(tempfile.mkdtemp(prefix='ingestls-'))

        try:
            porcelain.clone(
                source=url,
                target=str(target),
                depth=self.depth,
                branch=ref.encode() if ref else None,
            )
        except Exception as error:
            shutil.rmtree(target, ignore_errors=True)
            raise GitHubAPIException(f'Falha ao clonar {url}: {error}') from error

        return target

    def cleanup(self, target: Path) -> None:
        shutil.rmtree(target, ignore_errors=True)
