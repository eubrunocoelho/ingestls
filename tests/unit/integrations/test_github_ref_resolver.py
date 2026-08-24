from types import SimpleNamespace

import pytest

from src.enums.github_url_type_enum import GitHubURLTypeEnum
from src.exceptions.github.github_api_exception import GitHubAPIException
from src.integrations.github_ref_resolver import GitHubRefResolver

OWNER = 'eubrunocoelho'
REPOSITORY = 'ingestls'

# SHA de 40 caracteres hexadecimais == formato válido, não precisa
# corresponder a um commit real, já que a detecção de COMMIT é puramente
# local (regex), sem consultar o GitHub.
VALID_SHA = 'dfe6e8f103f96233d6f65a67edfa43845ca3d159'


def _fake_refs(*, branches: list[str] | None = None, tags: list[str] | None = None) -> SimpleNamespace:
    # Constrói um objeto compatível com o retorno de `porcelain.ls_remote()`,
    # que expõe `.refs` como um `dict[bytes, bytes]` (nome completo da `ref -> sha`).
    refs = {}

    for name in branches or []:
        refs[f'refs/heads/{name}'.encode()] = b'0' * 40

    for name in tags or []:
        refs[f'refs/tags/{name}'.encode()] = b'0' * 40

    return SimpleNamespace(refs=refs)


@pytest.fixture
def resolver() -> GitHubRefResolver:
    return GitHubRefResolver()


def test_resolves_commit_via_sha_without_calling_ls_remote(resolver, mocker):
    # Um segmento que "parece" um SHA de commit (40 chars hex) e resolvido
    # localmente via `regex` -- NUNCA deveria chamar `ls_remote`, já que
    # precisa consultar o GitHub para reconhecer o formato.
    ls_remote = mocker.patch('src.integrations.github_ref_resolver.porcelain.ls_remote')

    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            VALID_SHA,
        )
    )

    assert result == (GitHubURLTypeEnum.COMMIT, VALID_SHA, None)
    ls_remote.assert_not_called()


def test_resolves_commit_with_residual_path(resolver, mocker):
    # Segmentos após o SHA formar o `path` residual (ex.: `tree/<sha>/src`).
    ls_remote = mocker.patch('src.integrations.github_ref_resolver.porcelain.ls_remote')

    result = resolver.resolve(OWNER, REPOSITORY, (VALID_SHA, 'src', 'github'))

    assert result == (GitHubURLTypeEnum.COMMIT, VALID_SHA, 'src/github')
    ls_remote.assert_not_called()


def test_resolves_branch_with_slash_in_the_name(resolver, mocker):
    # Cenário central: uma branch cujo nome contém `/` (ex.: `test/github-integration`)
    # não pode ser confundida com uma branch curta + path. O resolver precisa
    # tentar o prefixo MAIS LONGO primeiro para reconhecer o nome inteiro.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        return_value=_fake_refs(branches=['main', 'test/github-integration'])
    )

    result = resolver.resolve(OWNER, REPOSITORY, ('test', 'github-integration'))

    assert result == (GitHubURLTypeEnum.BRANCH, 'test/github-integration', None)


def test_resolves_branch_with_slash_and_residual_path(resolver, mocker):
    # Mesma branch de nome composto, mas agora com segmentos extras depois
    # dela -- devem virar o `path` residual, não fazer parte da referência.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        return_value=_fake_refs(branches=['test/github-integration']),
    )

    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            'test',
            'github-integration',
            'src',
            'github'
        ),
    )

    assert result == (GitHubURLTypeEnum.BRANCH, 'test/github-integration', 'src/github')


def test_resolves_simple_branch_without_slash(resolver, mocker):
    # Caso mais simples: uma branch com nome de um segmento só (`main`),
    # sem `/`. Serve de linha de base antes dos testes de branch composta
    # (`test/github-integration`), confirmando que o caso trivial também
    # funciona pelo mesmo algoritmo de prefixos.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        return_value=_fake_refs(branches=['main']),
    )

    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            'main',
        )
    )

    assert result == (GitHubURLTypeEnum.BRANCH, 'main', None)


def test_resolves_tag(resolver, mocker):
    # Confirma que um segmento presente em `refs/tags` (não em `refs/heads/`) é
    # classificado como `TAG`, não `BRANCH` -- é a distinção
    # que só é possível consultando o repositório real, já que sintaticamente
    # uma tag e uma branch são indistinguíveis na URL.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        return_value=_fake_refs(branches=['main'], tags=['v0.0.1-test']),
    )

    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            'v0.0.1-test',
        )
    )

    assert result == (GitHubURLTypeEnum.TAG, 'v0.0.1-test', None)


def test_prefers_branch_over_tag_when_names_collide(resolver, mocker):
    # Documenta a prioridade do algoritmo: se uma branch e uma tag tiverem
    # o mesmo nome (raro, mas possível no Git), o resolver escolhe BRANCH,
    # já que ela é checada primeiro no loop de prefixos.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        return_value=_fake_refs(branches=['v1.0'], tags=['v1.0']),
    )

    result = resolver.resolve(
        OWNER,
        REPOSITORY,
        (
            'v1.0',
        )
    )

    assert result == (GitHubURLTypeEnum.BRANCH, 'v1.0', None)


def test_raises_when_reference_is_not_found(resolver, mocker):
    # Caso de falha #1: `ls_remote` funciona normalmente e devolve `refs`
    # válidas (`main` existe), mas o segmento pedido não está entre elas.
    # O loop de prefixos esgota todas as tentativas sem achar nada, e o `resolver` levanta
    # `GitHubAPIException` informando que a referência não foi
    # encontrada -- diferente de `test_raises_when_ls_remote_fails`,
    # aqui a comunicação com o GitHub funcionou; só a referência em si
    # não existe no repositório.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        return_value=_fake_refs(branches=['main']),
    )

    with pytest.raises(GitHubAPIException):
        resolver.resolve(
            OWNER,
            REPOSITORY,
            (
                'does-not-exist',
            )
        )


def test_raises_when_ls_remote_fails(resolver, mocker):
    # Caso de falha #2: a própria chamada a `ls_remote` quebra (erro de
    # `rede`/`conexão`) -- diferente do teste anterior, aqui nem chegamos a ter
    # uma lista de `refs` para comparar. Confirma que o erro interno do `dulwich/requests`
    # é convertido para `GitHubAPIException`, sem vazar a exceção original para quem chamou.
    mocker.patch(
        'src.integrations.github_ref_resolver.porcelain.ls_remote',
        side_effect=ConnectionError('boom'),
    )

    with pytest.raises(GitHubAPIException):
        resolver.resolve(
            OWNER,
            REPOSITORY,
            (
                'main',
            )
        )


def test_raises_when_no_segments_are_given(resolver):
    # Caso de borda: uma tupla de segmentos vazia (nenhuma referência
    # informada) deve falhar cedo, antes mesmo de tentar consultar o
    # GitHub -- não faz sentido chamar `ls_remote` sem nada para resolver.
    with pytest.raises(GitHubAPIException):
        resolver.resolve(OWNER, REPOSITORY, ())
