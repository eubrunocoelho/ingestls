import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.file_matcher import FileMatcher


@pytest.fixture
def matcher() -> FileMatcher:
    return FileMatcher()


@pytest.fixture
def pattern() -> PatternDTO:
    return PatternDTO(
        pattern='index.php',
        value='index.php',
        kind=PatternKindEnum.FILE,
        scope=PatternScopeEnum.GLOBAL,
    )


def test_matches_file_with_the_exact_name(matcher, pattern):
    # Caso feliz: um arquivo cujo nome bate exatamente com `pattern.value`
    # deve casar.
    node = DirectoryNode(name='index.php', is_directory=False, children=[])

    assert matcher.matches(node, pattern) is True


def test_does_not_match_file_with_a_different_name(matcher, pattern):
    # Um arquivo de nome diferente, mesmo com a mesma extensão, não deve casar.
    node = DirectoryNode(name='cache.php', is_directory=False, children=[])

    assert matcher.matches(node, pattern) is False


def test_never_matches_a_directory_even_with_the_exact_same_name(matcher, pattern):
    # Caso adversário: uma pasta chamada `index.php` (incomum, mas possível)
    # não pode ser tratada como arquivo.
    node = DirectoryNode(name='index.php', is_directory=True, children=[])

    assert matcher.matches(node, pattern) is False


def test_is_case_sensitive(matcher, pattern):
    # Confirma que a comparação de nome é sensível a maiúsculas/minúsculas --
    # `INDEX.PHP` não deve casar com o padrão `index.php`.
    node = DirectoryNode(name='INDEX.PHP', is_directory=False, children=[])

    assert matcher.matches(node, pattern) is False
