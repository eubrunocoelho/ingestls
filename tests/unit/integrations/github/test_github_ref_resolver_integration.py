"""Teste de integração: batem no GitHub de verdade via `ls-remote` (protocolo
git, através do dulwich -- sem tocar a `REST API`, sem `rate limit`). Precisam de
acesso a internet e dependem do estado real do repositório `eubrunocoelho/ingestls`:
- branch `test/github-integration` (com `/` no nome, criada só para este teste)
- tag `v0.0.1-test`
- branch `main` (padrão)

Se a `branch`/`tag` de teste for removida do repositório, estes testes passam a
falhar -- nesse caso, recrie-as ou ajuste os nomes abaixo."""
import pytest

from src.enums.github_url_type_enum import GitHubURLTypeEnum
from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_ref_resolver import GitHubRefResolver

OWNER = 'eubrunocoelho'
REPOSITORY = 'ingestls'

TEST_BRANCH = 'test/github-integration'
TEST_TAG = 'v0.0.1-test'

# Um commit real do repositório (ajuste se o commit for removido/reescrito
# via rebase/force-push). Usado só para confirmar que um SHA válido de
# fato resolve como `COMMIT` -- a detecção em si é local, não depende deste
# commit realmente existir (ver observação no final do arquivo)
KNOWN_COMMIT_SHA = 'dfe6e8f103f96233d6f65a67edfa43845ca3d159'


@pytest.fixture
def resolver() -> GitHubRefResolver:
    return GitHubRefResolver()


def test_resolves_real_branch_with_slash_in_the_name(resolver):
    result = resolver.resolve(OWNER, REPOSITORY, tuple(TEST_BRANCH.split('/')))

    assert result == (GitHubURLTypeEnum.BRANCH, TEST_BRANCH, None)


def test_resolves_real_branch_with_slash_and_residual_path(resolver):
    segments = tuple(TEST_BRANCH.split('/')) + ('src', 'github')

    result = resolver.resolve(OWNER, REPOSITORY, segments)

    assert result == (GitHubURLTypeEnum.BRANCH, TEST_BRANCH, 'src/github')


def test_resolves_real_main_branch(resolver):
    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            'main',
        )
    )

    assert result == (GitHubURLTypeEnum.BRANCH, 'main', None)


def test_resolves_real_tag(resolver):
    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            TEST_TAG,
        )
    )

    assert result == (GitHubURLTypeEnum.TAG, TEST_TAG, None)


def test_resolves_valid_looking_commit_sha(resolver):
    # IMPORTANTE: está detecção é puramente local (`regex` de 40 chars hex),
    # o `resolver` nunca confirma junto ao GitHub se o commit realmente existe
    # no repositório. Um SHA válido no formato, mas inexistente, também
    # resolveria como `COMMIT` aqui -- a falha real (se houver) só apareceria depois,
    # ao tentar de fato clonar/fazer checkout desse `commit`.
    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            KNOWN_COMMIT_SHA,
        )
    )

    assert result == (GitHubURLTypeEnum.COMMIT, KNOWN_COMMIT_SHA, None)


def test_raises_for_a_reference_that_does_not_exist_in_the_real_repository(resolver):
    with pytest.raises(GitHubAPIException):
        resolver.resolve(
            OWNER,
            REPOSITORY,
            (
                'branch-that-doesn\'t-really-exist',
            )
        )
