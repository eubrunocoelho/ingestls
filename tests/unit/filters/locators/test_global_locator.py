import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.locators.global_locator import GlobalLocator
from src.filters.matchers.extension_matcher import ExtensionMatcher
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
def locator() -> GlobalLocator:
    return GlobalLocator()


@pytest.fixture
def pattern() -> PatternDTO:
    return PatternDTO(
        pattern='*.php',
        value='.php',
        kind=PatternKindEnum.EXTENSION,
        scope=PatternScopeEnum.GLOBAL,
    )


@pytest.mark.parametrize('current_path', [
    'Controller.php',  # raiz
    'app/Controller.php',  # 1º nível
    'app/Http/Controllers/Controller.php',  # 3º nível
])
def test_delegates_to_matcher_regardless_of_depth(locator, pattern, current_path):
    # Regressão de erro corrigido: `GLOBAL` precisa valer em qualquer profundidade,
    # não só na raiz.
    node = DirectoryNode(name='Controller.php', is_directory=False, children=[])
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
    node = DirectoryNode(name='style.css', is_directory=False, children=[])
    matcher = _StubMatcher(return_value=False)

    result = locator.matches(
        node=node,
        current_path='app/style.css',
        matcher=matcher,
        pattern=pattern,
    )

    assert result is False


def test_integration_with_real_extension_matcher_matches_nested_file():
    locator = GlobalLocator()
    matcher = ExtensionMatcher()
    pattern = PatternDTO(
        pattern='*.php',
        value='.php',
        kind=PatternKindEnum.EXTENSION,
        scope=PatternScopeEnum.GLOBAL,
    )
    node = DirectoryNode(name='User.php', is_directory=False, children=[])

    result = locator.matches(
        node=node,
        current_path='app/Models/User.php',
        matcher=matcher,
        pattern=pattern,
    )

    assert result is True
