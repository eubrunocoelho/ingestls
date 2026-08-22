import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.locators.recursive_locator import RecursiveLocator
from src.filters.matchers.file_matcher import FileMatcher
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
def locator() -> RecursiveLocator:
    return RecursiveLocator()


@pytest.fixture
def pattern() -> PatternDTO:
    return PatternDTO(
        pattern='*/cache.php',
        value='cache.php',
        kind=PatternKindEnum.FILE,
        scope=PatternScopeEnum.RECURSIVE,
    )


@pytest.mark.parametrize('current_path', [
    'cache.php',
    'other/cache.php',
    'nested/deep/cache.php',
])
def test_delegates_to_matcher_regardless_of_depth(locator, pattern, current_path):
    # Confirma que o `RecursiveLocator` delega ao `matcher` em qualquer
    # profundidade (raiz, 1 nível, 2 níveis) -- assim como o `GlobalLocator`,
    # ele nunca inspeciona `current_path` para decidir se repassa a chamada.
    # Hoje `GLOBAL` e `RECURSIVE` tem comportamento de locator idêntico; a
    # diferença de semântica entre os dois vem do `value` que a `PatternRule`
    # de origem calcula, não da lógica do locator em si.
    node = DirectoryNode(name='cache.php', is_directory=False, children=[])
    matcher = _StubMatcher(return_value=True)

    result = locator.matches(
        node=node,
        current_path=current_path,
        matcher=matcher,
        pattern=pattern,
    )

    assert result is True
    assert matcher.calls == [(node, pattern)]


def test_returns_false_when_matcher_returns_false(locator, pattern):
    # Confirma que o `RecursiveLocator` apenas repassa o resultado do `matcher`,
    # sem transformar `False` em `True` nem aplicar nenhuma lógica própria.
    node = DirectoryNode(name='readme.md', is_directory=False, children=[])
    matcher = _StubMatcher(return_value=False)

    result = locator.matches(
        node=node,
        current_path='docs/readme.md',
        matcher=matcher,
        pattern=pattern,
    )

    assert result is False


def test_integration_with_real_file_matcher_matches_at_any_depth_but_not_wrong_name():
    # Teste de integração (sem stub): usa o `FileMatcher` real para confirmar
    # dois comportamentos juntos -- um padrão `*/cache.php` (RECURSIVE) casa
    # `cache.php` em qualquer profundidade (`nested/deep/cache.php`), mas
    # continua rejeitando um arquivo de nome diferente (`loader.php`) mesmo
    # que o caminho também seja profundo (`vendor/package/loader.php`).
    locator = RecursiveLocator()
    matcher = FileMatcher()
    pattern = PatternDTO(
        pattern='*/cache.php',
        value='cache.php',
        kind=PatternKindEnum.FILE,
        scope=PatternScopeEnum.RECURSIVE,
    )

    matching_node = DirectoryNode(name='cache.php', is_directory=False, children=[])
    other_node = DirectoryNode(name='loader.php', is_directory=False, children=[])

    assert locator.matches(
        node=matching_node,
        current_path='nested/deep/cache.php',
        matcher=matcher,
        pattern=pattern,
    ) is True

    assert locator.matches(
        node=other_node,
        current_path='vendor/package/loader.php',
        matcher=matcher,
        pattern=pattern,
    ) is False
