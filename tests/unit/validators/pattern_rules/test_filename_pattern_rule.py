import pytest

from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.pattern_rules.filename_pattern_rule import FilenamePatternRule


@pytest.fixture
def rule() -> FilenamePatternRule:
    # Cria uma instância de regra de padrões de nome de arquivo.
    return FilenamePatternRule()


@pytest.mark.parametrize('pattern', [
    'index.php',
    'cache.php',
    'README.md',
    'style.css',
])
def test_matches_valid_filename_patterns(rule, pattern):
    # Reconhece nomes de arquivos com extensão no escopo global.
    result = rule.match(pattern)

    assert result is not None
    assert result.pattern == pattern
    assert result.value == pattern
    assert result.kind == PatternKindEnum.FILE
    assert result.scope == PatternScopeEnum.GLOBAL


def test_also_matches_extension_wildcard_pattern_due_to_permissive_regex(rule):
    # ATENÇÃO: a `regex/combinação` desta regra não excluí '*', então ela também
    # reconhece padrões como `*.php`. Quem impede que isso vire
    # `kind=FILE` em vez de `kind=EXTENSION` é a ordem das
    # regras dentro do `IngestPatternValidator` (`ExtensionPatternRule` vem antes).
    # Este teste documenta a sobreposição; a garantia de precedência
    # está em `test_ingest_pattern_validator.py` -- Documenta a sobreposição da regra
    # de arquivo com padrões de extensão.
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
    # Retorna `None` para padrões que não representam apenas um nome de arquivo.
    assert rule.match(pattern) is None
