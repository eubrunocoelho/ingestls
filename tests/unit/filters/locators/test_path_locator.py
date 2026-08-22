import pytest

from dataclasses import replace

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filters.locators.path_locator import PathLocator
from src.filters.matchers.file_matcher import FileMatcher
from src.dtos.pattern_dto import PatternDTO
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.matcher import Matcher


class _StubMatcher(Matcher):
    # `Matcher` falso usado para isolar a lógica do `locator` da `regex/comparação`
    # real do `matcher`. Registra as chamadas e devolve um valor fixo.
    def __init__(self, return_value: bool):
        self.return_value = return_value
        self.calls: list[tuple[DirectoryNode, PatternDTO]] = []

    def matches(self, node: DirectoryNode, pattern: PatternDTO) -> bool:
        self.calls.append((node, pattern))

        return self.return_value


@pytest.fixture
def locator() -> PathLocator:
    return PathLocator()


@pytest.fixture
def pattern() -> PatternDTO:
    return PatternDTO(
        pattern='app/cache.php',
        value='app/cache.php',
        kind=PatternKindEnum.FILE,
        scope=PatternScopeEnum.PATH,
    )


def test_delegates_to_matcher_when_current_path_matches_exactly(locator, pattern):
    # Quando `current_path` bate exatamente com `pattern.value`, o `PathLocator`
    # delega ao `matcher` -- mas reescreve `pattern.value` para `node.name` antes
    # de delegar (via `dataclasses.replace`), já que `current_path` sozinho já
    # provou a identidade completa do caminho; o `matcher` só precisa confirmar
    # o nome/tipo do próprio nó, não o caminho inteiro de novo.
    node = DirectoryNode(name='cache.php', is_directory=False, children=[])
    matcher = _StubMatcher(return_value=True)

    result = locator.matches(
        node=node,
        current_path='app/cache.php',
        matcher=matcher,
        pattern=pattern,
    )

    assert result is True

    expected_pattern = replace(pattern, value=node.name)
    assert matcher.calls == [(node, expected_pattern)]


def test_short_circuits_without_calling_matcher_when_path_differs(locator, pattern):
    # Comportamento chave do `PATH`: caminho errado nunca deve chegar
    # a perguntar ao `matcher`, independente do `nome/tipo` do `node`.
    # Mesmo o `_StubMatcher` estando configurado para sempre retornar `True`,
    # o resultado precisa ser `False` e `matcher.calls` precisa ficar vazio --
    # provando que o curto-circuito acontece antes de qualquer chamada ao matcher.
    node = DirectoryNode(name='cache.php', is_directory=False, children=[])
    matcher = _StubMatcher(return_value=True)  # mesmo retornando `True`, não deve ser usado

    result = locator.matches(
        node=node,
        current_path='other/cache.php',
        matcher=matcher,
        pattern=pattern,
    )

    assert result is False
    assert matcher.calls == []


def test_integration_with_real_file_matcher_distinguishes_same_filename_in_different_paths():
    # Este é o cenário central da `fixture`: `app/cache.php`, `other/cache.php` e
    # `nested/deep/cache.php` tem o MESMO nome de arquivo, mas só o primeiro deve casar
    # com o padrão `PATH` ancorado em `app/cache.php`. Usa o `FileMatcher` real (não
    # o stub) para confirmar esse comportamento de ponta a ponta: o mesmo `node`
    # (`cache.php`) é testado contra os 3 caminhos, e só o caminho idêntico ao
    # padrão deve resultar em `True`.
    locator = PathLocator()
    matcher = FileMatcher()
    pattern = PatternDTO(
        pattern='app/cache.php',
        value='app/cache.php',
        kind=PatternKindEnum.FILE,
        scope=PatternScopeEnum.PATH,
    )
    node = DirectoryNode(name='cache.php', is_directory=False, children=[])

    assert locator.matches(
        node=node,
        current_path='app/cache.php',
        matcher=matcher,
        pattern=pattern,
    ) is True

    assert locator.matches(
        node=node,
        current_path='other/cache.php',
        matcher=matcher,
        pattern=pattern,
    ) is False

    assert locator.matches(
        node=node,
        current_path='nested/deep/cache.php',
        matcher=matcher,
        pattern=pattern,
    ) is False
