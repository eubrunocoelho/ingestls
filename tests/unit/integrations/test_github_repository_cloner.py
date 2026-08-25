from pathlib import Path

import pytest

from src.integrations.github_repository_cloner import GitHubRepositoryCloner


def test_cleanup_retries_when_windows_reports_file_in_use(
        tmp_path: Path,
        monkeypatch,
):
    cloner = GitHubRepositoryCloner(
        base_dir=tmp_path,
    )

    target = tmp_path / 'ingestls-test'
    target.mkdir()

    attempts = 0

    # noinspection PyUnusedLocal
    def fake_rmtree(path, onexc):
        nonlocal attempts

        attempts += 1

        if attempts < 3:
            error = PermissionError(
                '[WinError 32] O arquivo já está sendo usado '
                'por outro processo.'
            )
            error.winerror = 32

            raise error

        path.rmdir()

    monkeypatch.setattr(
        'src.integrations.github_repository_cloner.shutil.rmtree',
        fake_rmtree,
    )

    monkeypatch.setattr(
        'src.integrations.github_repository_cloner.time.sleep',
        lambda _: None,
    )

    cloner.cleanup(
        target,
        retries=5,
        delay=0.2,
    )

    assert attempts == 3
    assert not target.exists()


def test_cleanup_does_not_retry_for_other_permission_errors(
        tmp_path: Path,
        monkeypatch,
):
    cloner = GitHubRepositoryCloner(
        base_dir=tmp_path,
    )

    target = tmp_path / 'ingestls-test'
    target.mkdir()

    attempts = 0

    # noinspection PyUnusedLocal
    def fake_rmtree(_path, onexc):
        nonlocal attempts

        attempts += 1

        error = PermissionError(
            '[WinError 5] Acesso negado'
        )
        error.winerror = 5

        raise error

    monkeypatch.setattr(
        'src.integrations.github_repository_cloner.shutil.rmtree',
        fake_rmtree,
    )

    with pytest.raises(PermissionError):
        cloner.cleanup(target)

    assert attempts == 1
    assert target.exists()


def test_cleanup_raises_after_max_retries(
        tmp_path: Path,
        monkeypatch,
):
    cloner = GitHubRepositoryCloner(
        base_dir=tmp_path,
    )

    target = tmp_path / 'ingestls-test'
    target.mkdir()

    attempts = 0

    # noinspection PyUnusedLocal
    def fake_rmtree(_path, onexc):
        nonlocal attempts

        attempts += 1

        error = PermissionError(
            '[WinError 32] O arquivo já está sendo usado '
            'por outro processo.'
        )
        error.winerror = 32

        raise error

    monkeypatch.setattr(
        'src.integrations.github_repository_cloner.shutil.rmtree',
        fake_rmtree,
    )

    monkeypatch.setattr(
        'src.integrations.github_repository_cloner.time.sleep',
        lambda _: None,
    )

    with pytest.raises(PermissionError):
        cloner.cleanup(
            target=target,
            retries=3,
            delay=0.2,
        )

    assert attempts == 3
    assert target.exists()
