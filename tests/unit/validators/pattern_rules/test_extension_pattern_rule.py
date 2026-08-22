import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.extension_pattern_rule import ExtensionPatternRule


@pytest.fixture
def rule() -> ExtensionPatternRule:
    # Cria uma instância da regra de padrões de extensão.
    return ExtensionPatternRule()


@pytest.mark.parametrize('pattern, expected_value', [
    ('*.php', '.php'),
    ('*.txt', '.txt'),
    ('*.PHP', '.PHP'),
    ('*.a1', '.a1'),
])
def test_matches_valid_extension_patterns(rule, pattern, expected_value):
    # Reconhece padrões de extensão global e extrai a extensão sem o `*`.
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == expected_value
    assert result.kind == PatternKindEnum.EXTENSION
    assert result.scope == PatternScopeEnum.GLOBAL


@pytest.mark.parametrize('pattern', [
    'index.php',  # sem `*` na frente
    '*.php.bak',  # extensão composta não suportada
    '*/cache.php',  # tem escopo recursivo, não extensão pura
    'app/cache.php',  # tem caminho, não extensão pura
    '*.',  # sem extensão de fato
    '*',  # sem extensão nenhuma
    '',  # vazio
    'vendor/',  # é um padrão de diretório
])
def test_does_not_match_invalid_patterns(rule, pattern):
    # Retorna `None` para padrões que não representam uma extensão global válida.
    assert rule.match(pattern) is None
