# Ingestls

**Ingestls** é uma _API REST_ em _Python_ que converte um diretório local _(Windows)_ ou um repositório do _GitHub_ em um **digest de texto único** — um documento consolidado contendo a estrutura de diretórios e o conteúdo de todos os arquivos relevantes, pronto para ser colado no _prompt de um LLM_ _(ChatGPT, Claude, etc.)_.

A ideia central: em vez de você (ou uma IA) precisar abrir arquivo por arquivo para entender um projeto, o `Ingestls` entrega tudo em um único bloco de texto, já filtrado, formatado e com um resumo estatístico no topo.

## Exemplo de resposta

```
Repositório/Diretório: eubrunocoelho/ingestls
Referência do GitHub: branch main
Diretórios: 65
Arquivos Analisados: 175
Linhas de Código: 6.556

Estimativa de Tokens: 56.0k
```

seguido da árvore de diretórios renderizada e do conteúdo de cada arquivo, delimitado por marcadores.

## Categoria de software

`Ingestls` se enquadra na categoria de **ferramentas de apoio a fluxos de trabalho com IA (LLM tooling)** — mais especificamente, um **gerador de digest de código-fonte** _(também chamado de "repo-to-text" ou "codebase flattener")_. É o mesmo tipo de ferramenta que [_Gitingest_](https://gitingest.com/) e [_Repomix_](https://repomix.com/), voltada para preparar contexto de código para modelos de linguagem — seja para revisão automatizada, documentação assistida por IA, ou simplesmente entender um projeto desconhecido rapidamente.

Tecnicamente, trata-se de uma **API HTTP desenvolvida com Flask**, estruturada seguindo uma **arquitetura em camadas** e dotada de uma **interface gráfica desenvolvida em HTML**.

## Como o projeto foi desenvolvido

O projeto foi construído de forma incremental, camada por camada, com testes unitários guiando cada decisão de design. A arquitetura segue alguns princípios centrais:

### Strategy Pattern para múltiplas origens

Existem hoje duas origens suportadas — _diretório local do Windows_ e _repositório do GitHub_ — cada uma implementada como uma `IngestStrategy` própria (`WindowsIngestStrategy`, `GitHubIngestStrategy`), coordenadas por um `IngestDispatcher` que escolhe a estratégia certa via `supports(dto)`. A classe base `IngestStrategy` usa **Template Method**: o fluxo comum (`processar padrões → escanear → filtrar → renderizar → ler conteúdo → montar resumo → limpar recursos`) vive em um único lugar; cada estratégia concreta só implementa os passos que realmente variam (`_resolve_target`, `_scan`, `_read_files`, `_describe_target`, `_describe_reference`, `_cleanup`).

### Filtragem baseada em regras compostas

Os padrões de _inclusão/exclusão_ (`*.php`, `vendor/`, `*/cache.php`, `app/cache.php`, etc.) são interpretados por uma cadeia de `PatternRule`s (uma por formato padrão: _extensão, nome de arquivo, diretório, caminho completo, e variantes recursivas_), cada uma usando uma expressão regular própria. O resultado é um `PatternDTO` tipado (`kind` + `scope`), que depois é resolvido em tempo de filtragem por uma combinação de `Locator` (decide **onde** o padrão se aplica: _globalmente, recursivamente, ou em um caminho exato_) e `Matcher` (decide **o que** compara: _extensão, nome de arquivo, ou nome de diretório_) — escolhidos dinamicamente via `LocatorFactory`/`MatcherFactory`.

O `TreeFilter` aplica essas regras de duas formas assimétricas:

- `exclude`: remove o que bate, preserva diretórios mesmo que fiquem vazios.
- `include`: mantém só o que bate (ou tem descendente que bate), _podando diretórios inteiros sem correspondência_ — e _preservando a subárvore inteira_, sem filtrar por dentro, quando um padrão de diretório bate diretamente.

### Contêiner de injeção de dependência próprio

Em vez de _um framework de DI externo_, o projeto usa um `DIContainer` simples (bindings `singleton`/`transient` com resolução por tipo), montado por um `AppServiceProvider` que registra e conecta todas as dependências por domínio _(web, filesystem, filtros, GitHub, resumo, ingestão)_.

### Validação em camadas

Toda requisição passa por validação de _schema_ _(Pydantic, na borda HTTP)_ e depois por regras de negócio específicas (`IngestRule`s: existência de diretório, formato de URL do GitHub), cada uma decidindo via `supports(dto)` se deve ou não se aplicar àquela requisição — o mesmo padrão de _"regra auto-descritiva"_ usado nos `PatternRule`s.

### Por que `dulwich` em vez da API REST do GitHub

Essa foi uma decisão arquitetural central do projeto, motivada por um problema real: a **API REST do GitHub tem rate limit agressivo** — 60 requisições/hora sem autenticação, 5.000/hora com token pessoal. Uma implementação inicial baseada em REST (buscar árvore via _Git Trees API_, depois de um `GET` por arquivo para obter conteúdo via _Contents/Blob API_) consumia esse limite rapidamente em repositórios de tamanho médio, e ficava ainda mais restritiva ao resolver referências ambíguas (branches com `/` no nome, como `renovate/algo-4.x`), que exigiam múltiplas tentativas de requisição só para descobrir onde a referência termina e o caminho começa.

A solução foi trocar o transporte: o **dulwich** é uma implementação pura em _Python_ do protocolo _Git_, permitindo `clone`/`ls-remote` diretamente pelo protocolo _smart HTTP_ do Git — um canal **completamente diferente e sem o mesmo rate limit** da _REST API_.

Vantagens práticas dessa escolha:

- **Sem rate limit relevante** para o volume de uso da ferramenta — `git clone`/`ls-remote` não competem pela mesma cota de _60-5.000 req/h_.

- **Uma única chamada `ls-remote`** já devolve _todas as branches e tags_ de uma vez (como _um dicionário nome → SHA_), permitindo resolver localmente, em memória, qual prefixo de segmentos da URL corresponde a uma referência real - sem precisar de uma requisição HTTP por tentativa.

- **Reuso total da lógica de leitura de disco**: _depois do clone, o repositório é só uma pasta local_ — o mesmo `WindowsDirectoryScanner`/`WindowsFileReader` usados para diretórios locais do usuário passam a servir também para _GitHub_, sem duplicar o código de varredura/leitura.

- **Sem dependência do binário `git`** instalado no sistema — o `dulwich` é uma _biblioteca Python pura_, o que simplifica a implantação _(nenhuma dependência externa de sistema operacional)_.

O _trade-off_ aceito: clonar um repositório (ainda que raso) é mais pesado em _I/O_ de disco do que buscar só _metadados via REST_ — mas para o caso de uso _(gerar um digest completo do conteúdo, não só metadados)_, o conteúdo inteiro precisaria ser baixado de qualquer forma.

## Funcionalidades

- **Ingestão de diretório local do Windows**, via caminho absoluto (`C:\...`).
- **Ingestão de repositório público do GitHub**, _via URL_ (`https://github.com/owner/repo`), com suporte a:
    - Referência específica: branch (inclusive nomes com `/`, como `feature/algo-4.x`), tag, ou commit SHA — `https://github.com/owner/repo/tree/<referência>`.
    - Subcaminho dentro da referência: `https://github.com/owner/repo/tree/<referência>/<subpasta>`.

- **Filtragem por padrões**, nos modos `include` (mantém só o que bate) e `exclude` (remove o que bate), suportando 6 combinações de escopo/tipo de padrão _(extensão, nome de diretório, nome de arquivo, caminho exato — cada um em escopo global ou recursivo)_.

- **Detecção de arquivo binário e vazio**, com _marcadores próprios no digest_ em vez de tentar decodificar conteúdo binário como texto.

- **Resumo estatístico (`summary`)** com: _identificação da origem, referência do GitHub (quando aplicável), quantidade de diretórios, quantidade de arquivos analisados, total de linhas de código, e estimativa de tokens_.

- **Renderização em árvore** da estrutura de diretórios filtrada, em _formato legível por humanos e por LLMs_.

## Ferramentas usadas no desenvolvimento

| Categoria                | Ferramenta                                                                                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Linguagem                | [Python 3.14](https://www.python.org/)                                                                                                                                                      |
| Framework web            | [Flask](https://flask.palletsprojects.com/)                                                                                                                                                 |
| Validação de schema      | [Pydantic](https://www.google.com/search?q=https://docs.pydantic.dev/)                                                                                                                      |
| Templates HTML           | [Jinja2](https://jinja.palletsprojects.com/)                                                                                                                                                |
| Protocolo Git            | [dulwich](https://www.dulwich.io/)                                                                                                                                                          |
| Testes                   | [pytest](https://docs.pytest.org/), [pytest-mock](https://pytest-mock.readthedocs.io/)                                                                                                      |
| Interface Web            | [HTML](https://developer.mozilla.org/pt-BR/docs/Web/HTML) / [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS) / [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) |
| Otimização de JavaScript | [Webpack.js](https://webpack.js.org/)                                                                                                                                                       |
| Formatação/lint          | [Ruff](https://docs.astral.sh/ruff/)                                                                                                                                                        |
| Controle de versão       | [Git](https://git-scm.com/) / [GitHub](https://github.com/)                                                                                                                                 |
| IDE                      | [PyCharm](https://www.jetbrains.com/pycharm/) / [VSCode](https://code.visualstudio.com/)                                                                                                    |

## Requisitos para rodar a aplicação

- **Sistema Operacional Windows** — obrigatório para a execução do projeto _(a ingestão de diretórios locais/repositórios do GitHub utiliza padrões específicos deste **SO *(Sistema Operacional)***)_

- **Python 3.14** (ou compatível — o projeto usa recursos recentes de tipagem, como `X | Y` em anotações e `slots=True` em `dataclasses`).

- **pip** para instalar as dependências.

- **Não é necessário ter o Git instalado no sistema** — toda interação com repositórios remotos é feita via `dulwich`, _biblioteca Python pura_.

- **Acesso à internet** para ingestão de repositórios do GitHub _(não necessário para diretórios locais)_.

### Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/Scripts/activate

# Instalar as dependências
pip install -r requirements.txt

# Rodar a aplicação
python main.py

# ou
py main.py
```

A API sobe por padrão em `http://127.0.0.1:5000`.

### Exemplo de uso via API

```bash
curl -X POST http://127.0.0.1:5000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "path": "https://github.com/owner/repo",
    "pattern": "*.php,vendor/,index.php",
    "pattern_type": "exclude"
  }'
```

### Rodar os testes

```bash
pytest -v
```
