from pathlib import Path

import pytest

from src.filesystem.directory_node import DirectoryNode
from src.filesystem.windows_directory_scanner import WindowsDirectoryScanner

FIXTURE_ROOT = Path(__file__).parents[2] / 'fixtures' / 'sample_project'

# Espelha exatamente o `$ ls -laR` real da `fixture` (verdade fundamental dos testes).
# Chave = caminho relativo, valor = `is_directory`.
EXPECTED_FIXTURE_ENTRIES: dict[str, bool] = {
    'app': True,
    'app/Http': True,
    'app/Http/Controllers': True,
    'app/Http/Controllers/Controller.php': False,
    'app/Http/Middleware': True,
    'app/Http/Middleware/HandleInertiaRequests.php': False,
    'app/Models': True,
    'app/Models/User.php': False,
    'app/Providers': True,
    'app/Providers/AppServiceProvider.php': False,
    'app/vendor': True,
    'app/vendor/autoload.php': False,
    'app/cache.php': False,
    'docs': True,
    'docs/readme.md': False,
    'index.php': False,
    'nested': True,
    'nested/deep': True,
    'nested/deep/cache.php': False,
    'other': True,
    'other/cache.php': False,
    'public': True,
    'public/assets': True,
    'public/assets/style.css': False,
    'public/index.php': False,
    'vendor': True,
    'vendor/package': True,
    'vendor/package/loader.php': False,
}


def _flatten(node: DirectoryNode, current_path: str = '') -> dict[str, bool]:
    # Achata a árvore em `{caminho_relativo: is_directory}`, ignorando o próprio `root`.
    entries: dict[str, bool] = {}

    for child in node.children:
        child_path = child.name if not current_path else f'{current_path}/{child.name}'
        entries[child_path] = child.is_directory

        if child.is_directory:
            entries.update(_flatten(child, child_path))

    return entries


@pytest.fixture
def scanner() -> WindowsDirectoryScanner:
    return WindowsDirectoryScanner()


class _FakeRootPath:
    # Substituto mínimo de `Path`, usado só para exercitar o `fallback`
    # de nome (`root.name` vazio, como acontece na raiz de um `drive` tipo `C:\\`).
    def __init__(self, name: str, is_dir_value: bool):
        self.name = name
        self._is_dir_value = is_dir_value

    def is_dir(self) -> bool:
        return self._is_dir_value

    def __str__(self) -> str:
        return 'C:\\'


# --- casos isolados, construídos com `tmp_path` ---
def test_returns_leaf_node_for_a_single_file(scanner, tmp_path):
    # Cria um arquivo solto (sem diretório pai relevante) e confirma que o
    # scanner devolve um nó folha: `is_directory=False` e `children=[]`.
    # Cobre o caso base de `_build` quando `root.is_dir()` é `False` --
    # não depende da fixture `sample_project`.
    file_path = tmp_path / 'notes.txt'
    file_path.write_text('hello')

    result = scanner.read(file_path)

    assert result.name == 'notes.txt'
    assert result.is_directory is False
    assert result.children == []


def test_returns_directory_node_with_no_children_for_empty_directory(scanner, tmp_path):
    # Cria um diretório vazio e confirma `is_directory=True`, `children=[]`.
    # Cobre o caso em que `root.iterdir()` não devolve nenhum item.
    empty_dir = tmp_path / 'empty'
    empty_dir.mkdir()

    result = scanner.read(empty_dir)

    assert result.name == 'empty'
    assert result.is_directory is True
    assert result.children == []


def test_builds_nested_tree_recursively(scanner, tmp_path):
    # Monta uma árvore própria (src/main.py, src/utils/helpers.py, readme.md)
    # e confirma via `_flatten` que a recursão desce corretamente em
    # múltiplos níveis. Independente da fixture -- valida só a mecânica
    # de recursão do `_build`.
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src' / 'main.py').write_text('print(1)')
    (tmp_path / 'src' / 'utils').mkdir()
    (tmp_path / 'src' / 'utils' / 'helpers.py').write_text('pass')
    (tmp_path / 'readme.md').write_text('# readme')

    result = scanner.read(tmp_path)

    assert _flatten(result) == {
        'src': True,
        'src/main.py': False,
        'src/utils': True,
        'src/utils/helpers.py': False,
        'readme.md': False,
    }


def test_sorts_directories_before_files_case_insensitively(scanner, tmp_path):
    # Cria nomes propositalmente misturados em maiúsculas/minúsculas para
    # confirmar a chave de ordenação usada em `_build`: `(p.is_file(), p.name.lower())`.
    # Diretórios primeiro (ordem alfabética case-insensitive: apple, Cherry),
    # depois arquivos (ordem alfabética case-insensitive: aardvark.txt, Banana.txt).
    (tmp_path / 'Banana.txt').write_text('')
    (tmp_path / 'aardvark.txt').write_text('')
    (tmp_path / 'Cherry').mkdir()
    (tmp_path / 'apple').mkdir()

    result = scanner.read(tmp_path)

    assert [child.name for child in result.children] == [
        'apple', 'Cherry', 'aardvark.txt', 'Banana.txt'
    ]


def test_falls_back_to_str_when_root_has_no_name(scanner):
    # Usa o `_FakeRootPath` (objeto mínimo, não um `Path` de verdade) para
    # simular a raiz de um drive Windows (`root.name == ''`), confirmando
    # o fallback `str(root)` usado em `_build` quando o nome está vazio.
    fake_root = _FakeRootPath(name='', is_dir_value=False)

    result = scanner.read(fake_root)  # type: ignore[arg-type]

    assert result.name == 'C:\\'
    assert result.is_directory is False
    assert result.children == []


# --- integração com a `fixture` real ---
def test_scans_the_real_sample_project_fixture_completely(scanner):
    # Teste mais importante desta suíte: varre `tests/fixtures/sample_project`
    # de verdade (disco real, não `tmp_path`) e compara a árvore achatada
    # (`_flatten`) inteira contra `EXPECTED_FIXTURE_ENTRIES`, que espelha
    # exatamente a saída de `$ ls -ltR` sobre a fixture. Garante que nenhum
    # arquivo/diretório real fica de fora e que nenhum item extra aparece.
    if not FIXTURE_ROOT.exists():
        pytest.skip(f'`Fixture` não encontrada em {FIXTURE_ROOT}')

    result = scanner.read(FIXTURE_ROOT)

    assert result.name == 'sample_project'
    assert result.is_directory is True
    assert _flatten(result) == EXPECTED_FIXTURE_ENTRIES


def test_sample_project_root_children_are_sorted_dirs_first_then_files(scanner):
    # Confirma a ordem dos filhos diretos da raiz da fixture: os 6 diretórios
    # (app, docs, nested, other, public, vendor) em ordem alfabética, seguidos
    # do único arquivo da raiz (index.php). Bate com `$ ls -ltR` da raiz.
    if not FIXTURE_ROOT.exists():
        pytest.skip(f'`Fixture` não encontrada em {FIXTURE_ROOT}')

    result = scanner.read(FIXTURE_ROOT)

    assert [child.name for child in result.children] == [
        'app',
        'docs',
        'nested',
        'other',
        'public',
        'vendor',
        'index.php',
    ]


def test_sample_project_app_children_are_sorted_dirs_first_then_files(scanner):
    # Confirma a ordem dos filtros de `app/`: os 4 diretórios (Http, Models,
    # Providers, vendor) em ordem alfabética case-insensitive, seguidos do
    # único arquivo (cache.php). Bate com `$ ls -ltR` de `./app`.
    if not FIXTURE_ROOT.exists():
        pytest.skip(f'`Fixture` não encontrada em {FIXTURE_ROOT}')

    result = scanner.read(FIXTURE_ROOT)
    app_node = next(child for child in result.children if child.name == 'app')

    assert [child.name for child in app_node.children] == [
        'Http',
        'Models',
        'Providers',
        'vendor',
        'cache.php',
    ]
