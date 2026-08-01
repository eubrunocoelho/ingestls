import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.locators.recursive_locator import RecursiveLocator
from src.filters.matchers.file_matcher import FileMatcher
from src.filters.matchers.matcher import Matcher


class _StubMatcher(Matcher):
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
