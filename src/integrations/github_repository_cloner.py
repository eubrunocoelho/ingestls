import shutil
import tempfile
from pathlib import Path

from dulwich import porcelain

from src.exceptions.github.github_api_exception import GitHubAPIException


class GitHubRepositoryCloner:
    def __init__(self, base_dir: Path, depth: int = 1):
        self.base_dir = base_dir
        self.depth = depth

        self.base_dir.mkdir(parents=True, exist_ok=True)

    def clone(self, url: str, ref: str | None = None) -> Path:
        target = Path(tempfile.mkdtemp(prefix='ingestls-', dir=self.base_dir))

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

    @staticmethod
    def cleanup(target: Path) -> None:
        shutil.rmtree(target, ignore_errors=True)
