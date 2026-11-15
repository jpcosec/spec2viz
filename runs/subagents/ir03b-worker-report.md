# Informe IR03b: specIR monta sus tools de dominio sobre sldb mcp y borra su servidor MCP

## Commits (IR main, sin push: IR no tiene remoto)

- `3acb087`: código, tests, pyproject, decisiones en la tarea, preflight y bundle aceptados.
- `4b21433`: desk. Se retiran las 14 materializaciones que apuntaban a archivos borrados y se quitan de la tarea las rutas a tests borrados.
- `b34e2d0`: `deskops closeout resolved-by` (ref 3acb087; tests test_mcp_extension, test_imports, models/test_domain_tools).
- Este informe va en un commit aparte después de b34e2d0.

## Extensión

`specir.mcp_extension:register` (`src/specir/mcp_extension.py`). Se arranca con `sldb mcp --store <p>/.sldb --level N --actor A --extension specir.mcp_extension:register`.

- `specir_types`: solo lectura, en todos los niveles. Lista los tipos de dominio de IR06 con su capa, sus campos propios, si el store los registra y cuántos documentos tiene. Viene paginado.
- `specir_nodes`: solo lectura, en todos los niveles. Lista los nodos de specIR con su procedencia (origen, verificacion, verificado_por, evidencia, desconocidos). Se filtra por `kind`, `layer`, `origen` y `verificacion`, y viene paginado. Si el tipo no existe, devuelve la señal `unknown_model` con sugerencias, que queda en `list_signals`.
- Desde nivel 1, la extensión vuelve a servir `propose_changes` y `apply_changes` desde un único `WriteTools` de sldb. Antes de proponer aplica `claims_verified` (IR05 D2-E: un agente no escribe `verificacion: verificado`). Era lo único de dominio en `specir.mcp`, y sldb no lo migró a propósito. Para hacerlo usa `server.remove_tool` y `server.add_tool`. Así el sello que crea propose lo acepta apply.
- Imports: es el único módulo de specIR que alcanza `sldb.mcp` (changes, paging, registry, write). No importa `mcp` directamente. El resto de specIR solo usa `sldb.api`.

## Qué se borró (`git rm`) y su equivalente en sldb

| IR borrado | sldb (ce0a854e, en origin de09290c) |
| --- | --- |
| src/specir/mcp/__init__.py | src/sldb/mcp/__init__.py |
| src/specir/mcp/paging.py | src/sldb/mcp/paging.py |
| src/specir/mcp/addresses.py | src/sldb/mcp/addresses.py |
| src/specir/mcp/mutability.py | src/sldb/mcp/mutability.py |
| src/specir/mcp/changes.py | src/sldb/mcp/changes/ |
| src/specir/mcp/read_tools.py | src/sldb/mcp/read/ |
| src/specir/mcp/write_tools.py | src/sldb/mcp/write/ (claims_verified → specir.mcp_extension) |
| src/specir/mcp/server.py | src/sldb/mcp/server.py, signal_server, guard, registry, unmet, context, extension |
| tests/mcp/test_dry_run.py (1 test) | tests/mcp/test_dry_run.py (1) |
| tests/mcp/test_mutability.py (7) | tests/mcp/test_mutability.py (7) |
| tests/mcp/test_no_writes.py (1) | tests/mcp/test_no_writes.py (2). La parte federada pasa a IR tests/test_mcp_extension.py |
| tests/mcp/test_read_tools.py (13) | tests/mcp/test_read_tools.py (12). `test_spec_view_from_the_spec2viz_federation` no tiene par y pasa a IR tests/test_mcp_extension.py |
| tests/mcp/test_write_tools.py (9) | tests/mcp/test_write_tools.py (9, mismos nombres) |
| tests/mcp/writing.py | tests/mcp/mcp_helpers.py + mcp_world.py |

Otros cambios:

- En pyproject se quita el script `specir-mcp`. Los extras `mcp` y `test` pasan a depender de `structuredLanguageDB[mcp]`.
- tests/conftest.py levanta `python -m sldb mcp --extension specir.mcp_extension:register`. Se quitan los fixtures `write_copy`, `writer` y `content_writer`, que solo usaban los tests borrados.

## Tests nuevos

- `tests/test_imports.py` (4): ningún módulo de specIR salvo la extensión alcanza `mcp` o `sldb.mcp`; no queda servidor propio ni el script `specir-mcp`.
- `tests/test_mcp_extension.py` (5): cliente MCP real por stdio contra `sldb mcp` con la extensión, sobre una copia aislada en /dev/shm del store de IR, federado con deskops y spec2viz.
  - Comprueba que se sirven las tools de sldb y las de dominio.
  - A nivel 0 no existen `propose_changes` ni `apply_changes`; llamar a una devuelve la señal `unknown_tool`.
  - Se lee el SpecDoc de spec2viz enlazado.
  - Llamar a todas las tools no cambia el hash de la copia, ni de los stores enlazados, ni del store del repo.
- `tests/models/test_domain_tools.py` (5): `specir_types` y `specir_nodes` sobre el store del blog, con los filtros, la señal y las write tools de la extensión a nivel 1.

## Tests de IR, de a uno bajo /dev/shm/sldb1-tests.lock (TMPDIR=/dev/shm)

| archivo | rc | resultado |
| --- | --- | --- |
| tests/models/test_blog_chain.py | 0 | 7 passed, 2 xfailed (los 2 xfail strict ya existían) |
| tests/models/test_domain_models.py | 0 | 7 passed |
| tests/models/test_domain_tools.py | 0 | 5 passed |
| tests/test_imports.py | 0 | 4 passed |
| tests/test_mcp_extension.py | 0 | 5 passed |

## Revisiones

- Preflight 1: 4 ambigüedades. Se resolvieron en `implementation_path` ("Decisiones (preflight 1)") y se aceptó.
- Bundle 1: 4 ambigüedades. Se resolvieron en "Decisiones (bundle 1)" y se aceptó.

## deskops graph missing

`18 missing, 0 informational` (rc 1). Son las mismas 18 de antes: ir07 (3), ir12 (4), ir13 (3) e ir13d (4), todas de docs y tests visuales que aún no existen. No hay faltantes nuevos.

Tras el commit de código aparecieron 15 nuevos: 14 materializaciones que apuntaban a src/specir/mcp y tests/mcp, más una ruta citada en el texto de la tarea. Las materializaciones se retiraron con `deskops retire` (ref 3acb087) y la ruta se reescribió en la tarea.

## Entorno

En IR/.venv se instaló el sldb local editable con `uv pip install -e sldb[mcp]` y specIR con `.[test]`. Se reinstaló pytest, que se había caído al reinstalar specIR.

## Pendientes

- Para meter `claims_verified`, la extensión quita y vuelve a añadir las write tools e importa `sldb.mcp.write.WriteTools`. Convendría pedir a sldb un gancho público de comprobaciones de dominio antes de `propose_changes`, por ejemplo una lista de checks en `ServerContext`. No envié la nota al desk de sldb para no escribir en ese repo; queda para el coordinador (`deskops message send --to sldb`).
- `sldb.mcp` no forma parte de `sldb.api`. Se aceptó como contrato de extensión, solo en `mcp_extension.py`. Si sldb publica la paginación y las anotaciones en `sldb.api`, la extensión puede limitarse a eso.
- `src/specir.egg-info/` y los `__pycache__` quedan sin trackear; no están en .gitignore.
