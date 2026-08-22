import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.processors.pattern_set_processor import PatternSetProcessor
from src.validators.ingest_pattern_validator import IngestPatternValidator
from src.validators.pattern_rules.directory_pattern_rule import DirectoryPatternRule
from src.validators.pattern_rules.extension_pattern_rule import ExtensionPatternRule
from src.validators.pattern_rules.filename_pattern_rule import FilenamePatternRule
from src.validators.pattern_rules.path_filename_pattern_rule import PathFilenamePatternRule
from src.validators.pattern_rules.recursive_directory_pattern_rule import RecursiveDirectoryPatternRule
from src.validators.pattern_rules.recursive_filename_pattern_rule import RecursiveFilenamePatternRule


@pytest.fixture
def processor() -> PatternSetProcessor:
    validator = IngestPatternValidator(
        ExtensionPatternRule(),
        FilenamePatternRule(),
        DirectoryPatternRule(),
        PathFilenamePatternRule(),
        RecursiveDirectoryPatternRule(),
        RecursiveFilenamePatternRule(),
    )

    return PatternSetProcessor(validator)


@pytest.mark.parametrize('pattern', [None, ''])
def test_returns_empty_list_for_none_or_empty_string(processor, pattern):
    # `process(None)` e `process('')` devem devolver lista vazia sem tocar
    # no `validator` -- cobre o `if not pattern: return []` logo no início
    # do método, antes de qualquer `split`/`strip`.
    assert processor.process(pattern) == []


def test_returns_empty_list_for_blank_string(processor):
    # `split(',')` numa string só de espaços gera [' '], que após `strip()` vira
    # '' e é descartado antes de chegar no `validator`.
    assert processor.process(pattern='   ') == []


def test_parses_all_six_patterns_from_the_ticket_in_order(processor):
    # Teste principal: processa a string completa do `ticket` de uma vez e
    # confirma, em ordem, os 3 campos relevantes de cada `PatternDTO` gerado
    # (`kind`, `scope`, `value`) -- garantindo que os 6 padrões saem na
    # ordem exata em que apareceram na string original, sem embaralhar.
    raw = '*.php,vendor/,index.php,*/vendor/,*/cache.php,app/cache.php'

    result = processor.process(raw)

    assert [item.kind for item in result] == [
        PatternKindEnum.EXTENSION,
        PatternKindEnum.DIRECTORY,
        PatternKindEnum.FILE,
        PatternKindEnum.DIRECTORY,
        PatternKindEnum.FILE,
        PatternKindEnum.FILE,
    ]

    assert [item.scope for item in result] == [
        PatternScopeEnum.GLOBAL,
        PatternScopeEnum.GLOBAL,
        PatternScopeEnum.GLOBAL,
        PatternScopeEnum.RECURSIVE,
        PatternScopeEnum.RECURSIVE,
        PatternScopeEnum.PATH,
    ]

    assert [item.value for item in result] == [
        '.php', 'vendor', 'index.php', 'vendor', 'cache.php', 'app/cache.php',
    ]


def test_strips_whitespace_around_items_after_split(processor):
    # Confirma que espaços ao redor de cada item (antes/depois da vírgula)
    # são removidos pelo `strip()` -- ` *.php ` vira `*.php`, não fica com
    # espaço sobrando no `pattern` do `PatternDTO` resultante.
    raw = ' *.php , vendor/ , index.php '

    result = processor.process(raw)

    assert len(result) == 3
    assert result[0].pattern == '*.php'
    assert result[1].pattern == 'vendor/'
    assert result[2].pattern == 'index.php'


def test_skips_empty_items_between_consecutive_commas(processor):
    # Vírgulas duplicadas (`,,`) ou um item que vira uma string vazia após
    # `strip()` (`   `) devem ser silenciosamente ignorados, sem gerar
    # `PatternDTO` nenhum nem quebrar o processamento dos itens vizinhos.
    raw = '*.php,,vendor/,   ,index.php'

    result = processor.process(raw)

    assert [item.pattern for item in result] == ['*.php', 'vendor/', 'index.php']


def test_silently_skips_patterns_that_no_rule_recognizes(processor):
    # Quando nenhuma `PatternRule` reconhece o item (`validator.validate`
    # retorna `None`), o processor descarta o item silenciosamente -- sem
    # levantar exceção -- e continua processando o restante da lista.
    raw = '*.php,???invalid???,vendor/'

    result = processor.process(raw)

    # o item inválido não vira exceção nem `PatternDTO`, só é descartado
    assert [item.pattern for item in result] == ['*.php', 'vendor/']


def test_single_pattern_without_commas(processor):
    # Caso simples: uma única string sem vírgula nenhuma ainda deve produzir
    # uma lista de um `PatternDTO`, com todos os campos corretamente
    # preenchidos pela regra que a reconheceu (`ExtensionPatternRule`).
    result = processor.process('*.php')

    assert len(result) == 1
    assert result[0] == PatternDTO(
        pattern='*.php',
        value='.php',
        kind=PatternKindEnum.EXTENSION,
        scope=PatternScopeEnum.GLOBAL,
    )
