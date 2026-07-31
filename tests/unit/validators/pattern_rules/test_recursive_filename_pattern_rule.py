import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.recursive_filename_pattern_rule import RecursiveFilenamePatternRule


@pytest.fixture
def rule() -> RecursiveFilenamePatternRule:
    return RecursiveFilenamePatternRule()


@pytest.mark.parametrize('pattern, expected_value', [
    ('*/cache.php', 'cache.php'),
    ('*/index.php', 'index.php'),
    ('*/README.md', 'README.md'),
])
def test_matches_valid_recursive_filename_patterns(rule, pattern, expected_value):
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == expected_value
    assert result.kind == PatternKindEnum.FILE
    assert result.scope == PatternScopeEnum.RECURSIVE


@pytest.mark.parametrize('pattern', [
    'cache.php',  # sem o prefixo `*/`, e escopo global
    'app/cache.php',  # tem caminho explícito, e escopo `PATH`
    '*/vendor/',  # é um padrão de diretório
    '',  # vazio
])
def test_does_not_match_invalid_patterns(rule, pattern):
    assert rule.match(pattern) is None
