import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.filename_pattern_rule import FilenamePatternRule


@pytest.fixture
def rule() -> FilenamePatternRule:
    return FilenamePatternRule()


@pytest.mark.parametrize('pattern', [
    'index.php',
    'cache.php',
    'README.md',
    'style.css',
])
def test_matches_valid_filename_patterns(rule, pattern):
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == pattern
    assert result.kind == PatternKindEnum.FILE
    assert result.scope == PatternScopeEnum.GLOBAL


def test_also_matches_extension_wildcard_pattern_due_to_permissive_regex(rule):
    # ATENÇÃO: a `regex` desta regra não excluí '*', então ela também
    # reconhece padrões como `*.php`. Quem impede que isso vire
    # `kind=FILE` em vez de `kind=EXTENSION` é a ORDEM das
    # regras dentro do `IngestPatternValidator` (`ExtensionPatternRule` vem antes).
    # Este teste documenta a sobreposição; a garantia de precedência esta em
    # `test_ingest_pattern_validator.py`
    result = rule.match('*.php')

    assert result is not None
    assert result.kind == PatternKindEnum.FILE


@pytest.mark.parametrize('pattern', [
    'app/cache.php',  # tem caminho, não é só o nome do arquivo
    '*/cache.php',  # escopo recursivo, regra diferente
    'vendor/',  # é um padrão de diretório
    'noextension',  # sem extensão
    '',  # vazio
])
def test_does_not_match_invalid_patterns(rule, pattern):
    assert rule.match(pattern) is None
