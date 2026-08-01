import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.directory_matcher import DirectoryMatcher


@pytest.fixture
def matcher() -> DirectoryMatcher:
    return DirectoryMatcher()


@pytest.fixture
def pattern() -> PatternDTO:
    return PatternDTO(
        pattern='vendor/',
        value='vendor',
        kind=PatternKindEnum.DIRECTORY,
        scope=PatternScopeEnum.GLOBAL
    )


def test_matches_directory_with_the_exact_name(matcher, pattern):
    node = DirectoryNode(name='vendor', is_directory=True, children=[])

    assert matcher.matches(node, pattern) is True


def test_does_not_match_directory_with_a_different_name(matcher, pattern):
    node = DirectoryNode(name='node_modules', is_directory=True, children=[])

    assert matcher.matches(node, pattern) is False


def test_never_matches_a_file_even_with_the_exact_same_name(matcher, pattern):
    # Caso adversário: um arquivo chamado literalmente `vendor` (sem extensão)
    # não pode ser tratado como diretório
    node = DirectoryNode(name='vendor', is_directory=False, children=[])

    assert matcher.matches(node, pattern) is False


def test_ignores_the_directories_own_children_only_compares_the_name(matcher, pattern):
    # O `matcher` não deve se importar com o conteúdo do diretório, só com `nome/tipo`.
    node = DirectoryNode(
        name='vendor',
        is_directory=True,
        children=[DirectoryNode(name='package', is_directory=True, children=[])],
    )

    assert matcher.matches(node, pattern) is True
