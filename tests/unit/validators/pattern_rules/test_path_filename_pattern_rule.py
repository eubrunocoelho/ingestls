import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.path_filename_pattern_rule import PathFilenamePatternRule


@pytest.fixture
def rule() -> PathFilenamePatternRule:
    return PathFilenamePatternRule()


@pytest.mark.parametrize('pattern', [
    'app/cache.php',
    'app/Http/Controllers/Controller.php',
    'public/index.php',
])
def test_matches_valid_path_patterns(rule, pattern):
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == pattern
    assert result.kind == PatternKindEnum.FILE
    assert result.scope == PatternScopeEnum.PATH


@pytest.mark.parametrize('pattern', [
    'cache.php',  # sem caminho, é só o nome do arquivo
    '*/cache.php',  # tem coringa, escopo recursivo e não `PATH`
    '*.php',  # é um padrão de extensão
    'vendor/',  # é um padrão de diretório
    '',  # vazio
])
def test_does_not_match_invalid_patterns(rule, pattern):
    assert rule.match(pattern) is None
