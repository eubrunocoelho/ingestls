import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.recursive_directory_pattern_rule import RecursiveDirectoryPatternRule


@pytest.fixture
def rule() -> RecursiveDirectoryPatternRule:
    return RecursiveDirectoryPatternRule()


@pytest.mark.parametrize('pattern, expected_value', [
    ('*/vendor/', 'vendor'),
    ('*/node_modules/', 'node_modules'),
    ('*/cache-dir/', 'cache-dir'),
])
def test_matches_valid_recursive_directory_patterns(rule, pattern, expected_value):
    # Confirma que padrões `*/<diretório>/` casam e que `value` sai sem o
    # prefixo `*/` nem a barra final -- só o nome do diretório.
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == expected_value
    assert result.kind == PatternKindEnum.DIRECTORY
    assert result.scope == PatternScopeEnum.RECURSIVE


@pytest.mark.parametrize('pattern', [
    'vendor/',  # sem o prefixo `*/`, e escopo global
    '*/app/vendor/',  # mais de um nível após o `*/` não é suportado
    '*/cache.php',  # é um padrão de arquivo, não de diretório
    '',  # vazio
])
def test_does_not_match_invalid_patterns(rule, pattern):
    # Cobre 4 formatos que essa regra deve rejeitar, cada um delegando
    # o reconhecimento para outra regra (ou nenhuma).
    assert rule.match(pattern) is None
