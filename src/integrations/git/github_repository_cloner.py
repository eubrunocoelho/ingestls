import shutil
from pathlib import Path
from tempfile import mkdtemp

from dulwich import porcelain


class GitHubRepositoryCloner:
    def clone(self, url: str) -> Path:
        target = Path(mkdtemp())

        try:
            porcelain.clone(
                source=url,
                target=target,
            )

            return target
        except Exception:
            shutil.rmtree(target)

            raise
