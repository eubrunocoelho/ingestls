import os
import shutil
import stat
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
            repo = porcelain.clone(
                source=url,
                target=str(target),
                depth=self.depth,
                branch=ref.encode() if ref else None,
            )

            repo.close()
        except Exception as error:
            self.cleanup(target)
            raise GitHubAPIException(f'Falha ao clonar {url}: {error}') from error

        return target

    def cleanup(self, target: Path) -> None:
        shutil.rmtree(target, onexc=self._force_remove_readonly)

    @staticmethod
    def _force_remove_readonly(func, path, exc) -> None:
        os.chmod(path, stat.S_IWRITE)
        func(path)
