import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.validators.ingest_pattern_validator import IngestPatternValidator
from src.validators.pattern_rules.directory_pattern_rule import DirectoryPatternRule
from src.validators.pattern_rules.extension_pattern_rule import ExtensionPatternRule
from src.validators.pattern_rules.filename_pattern_rule import FilenamePatternRule
from src.validators.pattern_rules.path_filename_pattern_rule import PathFilenamePatternRule
from src.validators.pattern_rules.pattern_rule import PatternRule
from src.validators.pattern_rules.recursive_directory_pattern_rule import RecursiveDirectoryPatternRule
from src.validators.pattern_rules.recursive_filename_pattern_rule import RecursiveFilenamePatternRule


class _AlwaysNoneRule(PatternRule):
    # Regra falsa usada para testar a orquestração do `validator`.
    def match(self, pattern: str) -> PatternDTO | None:
        # Nunca reconhece um padrão e sempre retorna None.
        return None


class _AlwaysMatchRule(PatternRule):
    # Regra falsa que sempre reconhece um padrão para testar precedência.
    def __init__(self, tag: str):
        # Inicializa a regra com uma identificação usada no `PatternDTO`.
        self.tag = tag
        self.calls = 0

    def match(self, pattern: str) -> PatternDTO | None:
        # Registra a chamada e retorna um `PatternDTO` identificado pela tag.
        self.calls += 1

        return PatternDTO(
            pattern=pattern,
            value=self.tag,
            kind=PatternKindEnum.FILE,
            scope=PatternScopeEnum.GLOBAL,
        )


@pytest.fixture
def real_validator() -> IngestPatternValidator:
    # Cria o `validator` com todas as regras na ordem de precedência usada pela aplicação.
    return IngestPatternValidator(
        ExtensionPatternRule(),
        FilenamePatternRule(),
        DirectoryPatternRule(),
        PathFilenamePatternRule(),
        RecursiveDirectoryPatternRule(),
        RecursiveFilenamePatternRule(),
    )


def test_returns_none_when_no_rule_matches():
    # Retorna `None` quando nenhuma regra reconhece o padrão informado.
    validator = IngestPatternValidator(_AlwaysNoneRule(), _AlwaysNoneRule())

    assert validator.validate('???invalid???') is None


def test_stops_at_first_rule_that_matches_and_does_not_call_the_rest():
    # Interrompe a validação na primeira regra que reconhece o padrão.
    first = _AlwaysMatchRule(tag='first')
    second = _AlwaysMatchRule(tag='second')

    validator = IngestPatternValidator(first, second)

    result = validator.validate('anything')

    assert result is not None
    assert result.value == 'first'
    assert first.calls == 1
    assert second.calls == 0


def test_returns_none_with_no_rules_registered():
    # Retorna `None` quando o `validator` não possui nenhuma regra registrada.
    validator = IngestPatternValidator()

    assert validator.validate('*.php') is None


@pytest.mark.parametrize('pattern, expected_kind, expected_scope, expected_value', [
    ('*.php', PatternKindEnum.EXTENSION, PatternScopeEnum.GLOBAL, '.php'),
    ('vendor/', PatternKindEnum.DIRECTORY, PatternScopeEnum.GLOBAL, 'vendor'),
    ('index.php', PatternKindEnum.FILE, PatternScopeEnum.GLOBAL, 'index.php'),
    ('*/vendor/', PatternKindEnum.DIRECTORY, PatternScopeEnum.RECURSIVE, 'vendor'),
    ('*/cache.php', PatternKindEnum.FILE, PatternScopeEnum.RECURSIVE, 'cache.php'),
    ('app/cache.php', PatternKindEnum.FILE, PatternScopeEnum.PATH, 'app/cache.php'),
])
def test_resolves_each_pattern_from_the_ticket_to_the_expected_dto(
        real_validator,
        pattern,
        expected_kind,
        expected_scope,
        expected_value
):
    # Converte cada formato de padrão suportado no `PatternDTO` correspondente.
    result = real_validator.validate(pattern)

    assert result is not None
    assert result.kind == expected_kind
    assert result.scope == expected_scope
    assert result.value == expected_value


def test_extension_wildcard_resolves_as_extension_and_not_as_filename(real_validator):
    # Trava a precedência entre `ExtensionPatternRule` e `FilenamePatternRule`:
    # ambas as regras casam com `*.php` (ver `test_filename_pattern_rule.py`),
    # mas a ordem de registro no `validator` deve garantir `kind=EXTENSION`.
    # Se este teste quebrar, a ordem das regras em `di_container.py` mudou
    # (ou a `regex` de `FilenamePatternRule` foi alterada) e o comportamento de `matching`
    # por extensão está comprometido -- Garante a precedência da regra de extensão
    # sobre a regra de nome de arquivo.
    result = real_validator.validate('*.php')

    assert result is not None
    assert result.kind == PatternKindEnum.EXTENSION
    assert result.scope == PatternScopeEnum.GLOBAL
    assert result.value == '.php'
