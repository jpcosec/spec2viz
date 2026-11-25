PASA

# Resultado del tester (IR04b, cierre: comparación del store y digest por API pública)

- task: `task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import`
- commit del ejecutor: `e5c575592a333fbd55ca6628beb9bdd732700e7d` — *IR04b cierre (intento 2): el store se compara por select_documents + sha256 del texto sin bloque sldb*
- archivos del commit: `tests/test_mcp_undo.py` (solo tests; no cambia código de `src/specir`).
- entorno: worktree limpio `/workspace/ir04b-test-e5c5755` en `e5c5755`, `PYTHONPATH=/workspace/ir04b-test-e5c5755/src`, `TMPDIR=/tmp`, `/mnt/ssd/proyectos/SLDB_1/IR/.venv/bin/python`. Se copiaron a ese worktree los `runs/subagents/*/run.md` que el `.sldb` referencia y que no forman parte del commit (no se modificó el commit ni el código bajo prueba).

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `pytest -q -p no:cacheprovider tests/test_mcp_undo.py` | **8 passed**, rc 0 (213 s), sin xfail |
| `pytest -q -p no:cacheprovider tests/test_mcp_extension.py` | **11 passed**, rc 0 (117 s) |
| `pytest -q -p no:cacheprovider tests/models/test_blog_chain.py` | **7 passed, 2 xfailed**, rc 0 (14 s) |
| `pytest -q -p no:cacheprovider tests/models/test_domain_tools.py` | **5 passed**, rc 0 (11 s) |
| `pytest -q -p no:cacheprovider tests/test_imports.py` (extra) | **9 passed**, rc 0 (1 s) |

Los 2 xfailed de `test_blog_chain.py` son los preexistentes de aristas, ajenos a este cambio.

## Cumplimiento del encargo

1. **El store se compara por contenido antes y después de deshacer.** `md_digest` enumera los documentos trackeados con `sldb.api.select_documents(root / ".sldb", {})` (filas `export_id`, `model`, `name`, `path`, sin resolver modelos) y añade al digest, por cada documento, el sha256 de su archivo sin el bloque `sldb`, con clave estable `store:{export_id}@{path}`. El test de identidad (`test_the_documents_and_the_store_have_the_same_content_after_the_undo`) compara así el conjunto de claves y el contenido de cada documento antes/después. La prueba stale, que antes fallaba por `load_runtime_documents`, también pasa y compara el mismo digest.
2. **Sin imports internos en el digest.** El helper ya no importa `sldb.models.provenance_block` ni `strip_block`; solo usa `from sldb import api`. El resto de imports de `sldb.mcp.*` del archivo son preexistentes, pertenecen a otra prueba (registro/validadores de la extensión MCP) y no forman parte del helper de digest que pedía el encargo. `tests/test_imports.py` sigue verde.
3. **De a uno y en verde.** Los cuatro archivos exigidos por el encargo pasaron individualmente.

## Veredicto

**PASA.** El deshacer restaura el mismo contenido documental y el store se compara por el criterio acordado (`select_documents` + sha256 del texto sin bloque `sldb`); el digest usa solo la API pública `sldb.api`; los cuatro archivos de pruebas pasan de a uno.
