import os
import shutil
import stat
import tempfile
from pathlib import Path

from dulwich import porcelain
from dulwich.repo import Repo

from src.enums.github_url_type_enum import GitHubURLTypeEnum
from src.exceptions.github.github_api_exception import GitHubAPIException


class GitHubRepositoryCloner:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

        self.base_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def clone(
            self,
            url: str,
            ref: str | None = None,
            ref_type: GitHubURLTypeEnum | None = None,
    ) -> Path:
        target = Path(
            tempfile.mkdtemp(
                prefix='ingestls-',
                dir=self.base_dir,
            )
        )

        repo: Repo | None = None
        success = False

        try:
            clone_kwargs = {
                'source': url,
                'target': str(target)
            }

            if ref and ref_type in {
                GitHubURLTypeEnum.BRANCH,
                GitHubURLTypeEnum.TAG,
            }:
                clone_kwargs['branch'] = ref.encode()

            repo = porcelain.clone(**clone_kwargs)

            if ref and ref_type == GitHubURLTypeEnum.COMMIT:
                porcelain.checkout(
                    repo,
                    ref.encode(),
                )

            success = True

            return target

        except Exception as error:
            raise GitHubAPIException(
                f'Falha ao clonar {url}: {error}'
            ) from error

        finally:
            if repo is not None:
                repo.close()

            if not success:
                self.cleanup(target)

    def cleanup(self, target: Path) -> None:
        if not target.exists():
            return

        shutil.rmtree(
            target,
            onexc=self._force_remove_readonly
        )

    @staticmethod
    def _force_remove_readonly(func, path, exc) -> None:
        os.chmod(
            path,
            stat.S_IWRITE
        )

        func(path)
