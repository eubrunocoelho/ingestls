import pytest

from src.dtos.pattern_dto import PatternDTO
from src.enums.pattern_kind_enum import PatternKindEnum
from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filesystem.directory_node import DirectoryNode
from src.filters.factories.locator_factory import LocatorFactory
from src.filters.factories.matcher_factory import MatcherFactory
from src.filters.tree_filter import TreeFilter


def _dir(name: str, children: list[DirectoryNode] | None = None) -> DirectoryNode:
    return DirectoryNode(name=name, is_directory=True, children=children or [])


def _file(name: str) -> DirectoryNode:
    return DirectoryNode(name=name, is_directory=False, children=[])


def _flatten(node: DirectoryNode, current_path: str = '') -> dict[str, bool]:
    entries: dict[str, bool] = {}

    for child in node.children:
        child_path = child.name if not current_path else f'{current_path}/{child.name}'
        entries[child_path] = child.is_directory

        if child.is_directory:
            entries.update(_flatten(child, child_path))

    return entries


def _build_sample_project_tree() -> DirectoryNode:
    # Reproduz a árvore do `ticket` informado
    # (mesma saída do `WindowsDirectoryScanner` sobre `tests/fixtures/sample_project`).
    return _dir(
        'sample_project',
        [
            _dir(
                'app',
                [
                    _dir(
                        'Http',
                        [
                            _dir(
                                'Controllers',
                                [_file('Controller.php')]),
                            _dir(
                                'Middleware',
                                [_file('HandleInertiaRequests.php')]),
                        ]),
                    _dir(
                        'Models',
                        [_file('User.php')]),
                    _dir(
                        'Providers',
                        [_file('AppServiceProvider.php')]),
                    _dir(
                        'vendor',
                        [_file('autoload.php')]),
                    _file('cache.php'),
                ]),
            _dir(
                'docs',
                [_file('readme.md')]),
            _dir(
                'nested',
                [
                    _dir(
                        'deep',
                        [_file('cache.php')]),
                ]),
            _dir(
                'other',
                [_file('cache.php')]),
            _dir(
                'public',
                [
                    _dir(
                        'assets',
                        [_file('style.css')]),
                    _file('index.php'),
                ]),
            _dir(
                'vendor',
                [
                    _dir(
                        'package',
                        [_file('loader.php')]),
                ]),
            _file('index.php'),
        ]
    )


# Padrão de `ticket` para `*.php,vendor/,index.php,*/vendor/,*/cache.php,app/cache.php`
def _ticket_patterns() -> list[PatternDTO]:
    return [
        PatternDTO(
            pattern='*.php',
            value='.php',
            kind=PatternKindEnum.EXTENSION,
            scope=PatternScopeEnum.GLOBAL,
        ),
        PatternDTO(
            pattern='vendor/',
            value='vendor',
            kind=PatternKindEnum.DIRECTORY,
            scope=PatternScopeEnum.GLOBAL,
        ),
        PatternDTO(
            pattern='index.php',
            value='index.php',
            kind=PatternKindEnum.FILE,
            scope=PatternScopeEnum.GLOBAL,
        ),
        PatternDTO(
            pattern='*/vendor/',
            value='vendor',
            kind=PatternKindEnum.DIRECTORY,
            scope=PatternScopeEnum.RECURSIVE,
        ),
        PatternDTO(
            pattern='*/cache.php',
            value='cache.php',
            kind=PatternKindEnum.FILE,
            scope=PatternScopeEnum.RECURSIVE,
        ),
        PatternDTO(
            pattern='app/cache.php',
            value='app/cache.php',
            kind=PatternKindEnum.FILE,
            scope=PatternScopeEnum.PATH,
        ),
    ]


@pytest.fixture
def tree_filter() -> TreeFilter:
    return TreeFilter(LocatorFactory(), MatcherFactory())


# Tudo que deve sobrar depois de aplicar os 6 padrões: nenhum `.php`,
# nenhum diretório `vendor` (em qualquer profundidade), diretórios que ficaram vazios
# permanecem na árvore (o `TreeFilter` não poda diretório vazio).
EXPECTED_REMAINING_ENTRIES: dict[str, bool] = {
    'app': True,
    'app/Http': True,
    'app/Http/Controllers': True,
    'app/Http/Middleware': True,
    'app/Models': True,
    'app/Providers': True,
    'docs': True,
    'docs/readme.md': False,
    'nested': True,
    'nested/deep': True,
    'other': True,
    'public': True,
    'public/assets': True,
    'public/assets/style.css': False,
}


def test_exclude_removes_all_php_files_and_all_vendor_directories(tree_filter):
    tree = _build_sample_project_tree()
    patterns = _ticket_patterns()

    result = tree_filter.exclude(root=tree, patterns=patterns)

    assert _flatten(result) == EXPECTED_REMAINING_ENTRIES


def test_exclude_removes_root_level_vendor_directory_entirely(tree_filter):
    tree = _build_sample_project_tree()

    result = tree_filter.exclude(root=tree, patterns=_ticket_patterns())

    names = [child.name for child in result.children]
    assert 'vendor' not in names


def test_exclude_removes_nested_vendor_directory_entirely(tree_filter):
    tree = _build_sample_project_tree()

    result = tree_filter.exclude(root=tree, patterns=_ticket_patterns())

    app_node = next(child for child in result.children if child.name == 'app')
    names = [child.name for child in app_node.children]
    assert 'vendor' not in names


def test_exclude_keeps_directories_that_became_empty_after_filtering(tree_filter):
    # `app/Http/Controllers` só tinha `Controller.php`, que deve ser removido pelo
    # padrão de extensão -- mas o diretório em si permanece, vazio
    tree = _build_sample_project_tree()

    result = tree_filter.exclude(root=tree, patterns=_ticket_patterns())

    app_node = next(child for child in result.children if child.name == 'app')
    http_node = next(child for child in app_node.children if child.name == 'Http')
    controllers_node = next(child for child in http_node.children if child.name == 'Controllers')

    assert controllers_node.is_directory is True
    assert controllers_node.children == []


def test_exclude_keeps_files_that_do_not_match_any_pattern(tree_filter):
    tree = _build_sample_project_tree()

    result = tree_filter.exclude(root=tree, patterns=_ticket_patterns())

    docs_node = next(child for child in result.children if child.name == 'docs')
    public_node = next(child for child in result.children if child.name == 'public')
    assets_node = next(child for child in public_node.children if child.name == 'assets')

    assert [child.name for child in docs_node.children] == ['readme.md']
    assert [child.name for child in assets_node.children] == ['style.css']


def test_exclude_with_no_patterns_returns_tree_unchanged(tree_filter):
    tree = _build_sample_project_tree()
    original_flat = _flatten(tree)

    result = tree_filter.exclude(root=tree, patterns=[])

    assert _flatten(result) == original_flat


def test_exclude_does_not_mutate_unrelated_siblings(tree_filter):
    # Regressão simples: excluir `app/cache.php` via padrão `PATH` não deve
    # afetar `other/cache.php` nem `nested/deep/cache.php` (que só são
    # removidos pelos padrões `GLOBAL/RECURSIVE`, testados separadamente aqui
    # combinando só o padrão `PATH` isoladamente)
    tree = _build_sample_project_tree()
    path_only_pattern = [
        PatternDTO(
            pattern='app/cache.php',
            value='app/cache.php',
            kind=PatternKindEnum.FILE,
            scope=PatternScopeEnum.PATH,
        ),
    ]

    result = tree_filter.exclude(root=tree, patterns=path_only_pattern)

    app_node = next(child for child in result.children if child.name == 'app')
    other_node = next(child for child in result.children if child.name == 'other')
    nested_node = next(child for child in result.children if child.name == 'nested')
    deep_node = next(child for child in nested_node.children if child.name == 'deep')

    assert 'cache.php' not in [child.name for child in app_node.children]
    assert 'cache.php' in [child.name for child in other_node.children]
    assert 'cache.php' in [child.name for child in deep_node.children]
