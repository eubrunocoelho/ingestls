import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.matchers.extension_matcher import ExtensionMatcher


@pytest.fixture
def matcher() -> ExtensionMatcher:
    return ExtensionMatcher()


@pytest.fixture
def pattern() -> PatternDTO:
    return PatternDTO(
        pattern='*.php',
        value='.php',
        kind=PatternKindEnum.EXTENSION,
        scope=PatternScopeEnum.GLOBAL,
    )


@pytest.mark.parametrize('filename', [
    'Controller.php',
    'index.php',
    '.php',  # arquivo `oculto` cujo nome inteiro é a extensão
])
def test_matches_file_with_the_extension(matcher, pattern, filename):
    # Cobre 3 variações de nome que devem casar com `.php`: nome comum,
    # arquivo de entrada convencional, e o caso extremo de um arquivo cujo
    # nome inteiro é só a extensão (sem nada antes do ponto).
    node = DirectoryNode(name=filename, is_directory=False, children=[])

    assert matcher.matches(node, pattern) is True


def test_does_not_match_file_with_a_different_extension(matcher, pattern):
    # Um arquivo com outra extensão não deve casar com `.php`.
    node = DirectoryNode(name='style.css', is_directory=False, children=[])

    assert matcher.matches(node, pattern) is False


def test_never_matches_a_directory_even_if_the_name_ends_with_the_extension(matcher, pattern):
    # Caso adversário: um diretório chamado literalmente `vendor.php` não
    # pode ser tratado como arquivo só por causa do sufixo do nome.
    node = DirectoryNode(name='vendor.php', is_directory=True, children=[])

    assert matcher.matches(node, pattern) is False


def test_does_not_match_file_missing_the_extension_entirely(matcher, pattern):
    # Um arquivo sem extensão nenhuma (nome sem ponto) não deve casar.
    node = DirectoryNode(name='sREADME', is_directory=False, children=[])

    assert matcher.matches(node, pattern) is False
