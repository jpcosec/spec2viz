# Informe del worker de IR07

Tarea: `task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro` (documental, no migra código).

## Commits (IR main, sin push)

- `456b862` entregables: `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/gate-de-retiro.md`, `docs/decisiones/fuente-de-verdad-del-diagrama.md`, `tests/test_matriz_cobertura_spec2viz.py`.
- `1d331d2` desk: atom de la propuesta, `atoms`/`files`/`implementation_path` de la tarea (vía `deskops edit task`), reviews preflight-2 y bundle-2 dispuestas, runs de las revisiones [skip ci].
- `fcac582` closeout resolved-by (refs 456b862 y 1d331d2, test `tests/test_matriz_cobertura_spec2viz.py`).

## Matriz

105 filas (SV-*), revisión de spec2viz `2de1056` (v0.2.0; la ayuda del CLI coincide con `cli.py`), sldb en `641ecdfa`.

| Modo | Filas |
|---|---|
| migrar tal cual | 52 |
| migrado a sldb | 30 |
| usar sldb directamente | 19 |
| reemplazar | 4 |

Grupos: A modelos/carga/schema (17), B IR y compiladores (10), C renderers (15), D linter (1), E SpecSync (2), F generación (2), G catálogos (8), H notaciones/paletas/estilo (6), I emparejamiento de átomos (5), J API/recursos/about/habilidad (9), K comandos y subgrupos del CLI (30, uno por cada uno de los 29 que lista la ayuda más la ayuda raíz). También hay una tabla que asigna cada uno de los 38 archivos de `spec2viz/tests/` a sus filas, y una sección «Pendientes de derivación». Reemplazos: `catalog serve` por `sldb serve` (SV-G06, SV-K06), punto de entrada (SV-J07) y habilidad use-spec2viz por `skills/use-specir` (SV-J09).

## Consumidores inventariados

- graph_ui: `frontends/mindmap/sldb_adapter.py:245,437`, `pyproject.toml:19,24`, `.github/requirements-suite.txt:10`, `tests/test_projection_views.py`, `tests/test_mindmap_notation.py` y 8 e2e (`spec2viz diagram sync`).
- deskops: `deskops/graph/desk_graph.py:75` (regla de rutas), `desk/drawer/plans/workspace-documental/render_diagram.py:7,9`, `docs/diagrams/`, habilidades `.opencode/skills/use-spec2viz` y `.claude/skills/deskops-workflow` (`references/spec2viz-cli.md`).
- pron: `docs/spec2viz/build.py:22-24`.
- sldb: `docs/architecture/spec2viz/vistas.yml` y sus specs; `contracts/identity.toml:299`.
- IR: `tests/conftest.py:24,80` y `tests/test_mcp_extension.py:24` (federan el store de spec2viz).
- Stores: solo `spec2viz/.sldb` registra `spec2viz.sldb_models` (`store.yaml:44-57`, `core/store_index.yaml:141-194`, `core/models/*.yaml`).
- scion: sin dependencias. sldb-runtime y deskops-runtime se auditan por su repo de origen.

## Decisión del YAML frente al grafo

Atom `atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al` (five_wh_one_plus: how). **Estado: propuesta pendiente de JP.** AtomDoc no tiene campo de estado, así que el estado va en el título y en la respuesta. El detalle está en `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Recomendación: el YAML se queda de forma permanente como formato de autoría e intercambio, subordinado al grafo (sus elementos se anclan a las entidades y, si hay conflicto, gana el grafo). Lo que ya existe se dibuja como proyección. Para el diseño previo a la implementación, los elementos van sin ancla y se anclan cuando aparece la entidad. Los specs existentes se quedan donde están: durante la paridad sirven de fixtures y después cada repo decide por su desk. Se descartaron tres alternativas: el YAML como fuente, el YAML solo durante la paridad y autorar solo en el store. G7 del gate queda abierto hasta que JP decida.

## Revisiones

- preflight-2: 5 ambigüedades (revisión de spec2viz, ruta del plan, ids D1-D4, universo de repos, atom), resueltas en `implementation_path` y dispuestas como accepted.
- bundle-2: 4 ambigüedades (proponer o decidir, gate redactado o cumplido, recrear el atom, alcance de gate-de-retiro.md), resueltas en `implementation_path` y dispuestas como accepted.

## Tests (cada archivo por separado bajo `/dev/shm/sldb1-tests.lock`, TMPDIR=/dev/shm)

| Archivo | rc | Resultado |
|---|---|---|
| tests/test_matriz_cobertura_spec2viz.py | 0 | 5 passed |
| tests/test_imports.py | 0 | 4 passed |
| tests/test_mcp_extension.py | 0 | 5 passed |
| tests/models/test_blog_chain.py | 0 | 7 passed, 2 xfailed |
| tests/models/test_domain_models.py | 0 | 7 passed |
| tests/models/test_domain_tools.py | 0 | 5 passed |

El test nuevo lee `spec2viz/cli.py` por AST, porque spec2viz no se puede importar en IR/.venv; si se pudiera, usaría click. Comprueba los 29 comandos y subgrupos, los 22 módulos de compiladores, renderers, linters y generadores, los 38 archivos de pruebas, que cada fila tenga exactamente un modo y que ninguna fila esté descartada.

## graph missing

Bajó de 18 a **11**: IR07 resolvió los 7 faltantes que apuntaban a la matriz, al gate y a la decisión. Los que quedan son de IR12, IR13 e IR13d.

## Pendientes (no resueltos por IR07)

1. Las filas «usar sldb directamente» no tienen tarea que porte `test_notation`, `test_notation_view`, `test_view_contract_resolved`, `test_style_palette` ni `test_view_doc` contra sldb, porque IR13c se retiró. Las cubre IR13 o una tarea nueva.
2. sldb no tiene comando para validar una notación o una paleta por nombre o ruta (SV-K21, SV-K26). Falta pedirlo al desk de sldb; no envié el mensaje.
3. Falta decidir el CLI de validación de un spec (SV-K16 y SV-K29): o lo da sldb o el comando de specIR llama a `load_spec`.
4. D4 no incluye `tests/test_refs.py` (SV-I03).
5. La lista de archivos de IR12 no incluye `renderers/class_diagram.py` ni `renderers/view_mermaid.py` (SV-C13, SV-C14).
6. JP tiene que decidir sobre el atom de la propuesta (G7).

## Limpieza de /dev/shm

Borrado: `/dev/shm/ir07-tests.log`, `/dev/shm/ir07-one.log`, `/dev/shm/ir07-run-tests.sh`, `/dev/shm/ir07-paths.txt`, `/dev/shm/ir07-bundle.log` y `/dev/shm/ir07-specs-*.txt` (conteos de specs). No creé copias de stores ni basetemps propios; `/dev/shm/pytest-of-robocop` es compartido con otros procesos y no lo toqué.
