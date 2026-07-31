import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.directory_pattern_rule import DirectoryPatternRule


@pytest.fixture
def rule() -> DirectoryPatternRule:
    return DirectoryPatternRule()


@pytest.mark.parametrize('pattern, expected_value', [
    ('vendor/', 'vendor'),
    ('node_modules/', 'node_modules'),
    ('cache-dir/', 'cache-dir'),
    ('v1.0/', 'v1.0'),
])
def test_matches_valid_directory_patterns(rule, pattern, expected_value):
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == expected_value
    assert result.kind == PatternKindEnum.DIRECTORY
    assert result.scope == PatternScopeEnum.GLOBAL


@pytest.mark.parametrize('pattern', [
    'vendor',  # sem barra no final
    '*/vendor/',  # escopo recursivo, regra diferente
    'app/vendor/',  # caminho com mais de um nível não é suportado aqui
    '*.php',  # é um padrão de extensão
    '',  # vazio
])
def test_does_not_match_invalid_patterns(rule, pattern):
    assert rule.match(pattern) is None
