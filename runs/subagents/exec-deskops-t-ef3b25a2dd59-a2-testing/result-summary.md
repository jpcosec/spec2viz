FALLA

# Resultado del tester (IR04b, intento 2: deshacer por MCP sobre el lote inverso de sldb)

- task: `task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas`
- commit del ejecutor: `57616e89123162b9117109ad3fa5765f0ce960cf` — *IR04b intento 2: validación por contenido sin xfail; D2-E vuelve a error de herramienta en propose_changes*
- archivos del commit: `src/specir/mcp_extension.py`, `tests/test_mcp_extension.py`, `tests/test_mcp_undo.py`.
- entorno: worktree limpio `/workspace/ir04b-clean` en `57616e8`, `PYTHONPATH=/workspace/ir04b-clean/src`, `TMPDIR=/tmp`, `.venv/bin/python` del repo. Se copiaron al worktree los `runs/subagents/*/run.md` que el `.sldb` referencia (no están en el commit) para que la fixture `mount_copy` pudiera montar la copia; no se tocó el commit.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `pytest -q tests/test_mcp_undo.py` | **8 passed**, rc 0 (198 s), sin xfail. |
| `pytest -q tests/test_mcp_extension.py` | **11 passed**, rc 0 (117 s). |
| `pytest -q tests/models/test_blog_chain.py` | **7 passed, 2 xfailed**, rc 0 (14 s). |
| `pytest -q tests/models/test_domain_tools.py` | **5 passed**, rc 0 (11 s). |
| `pytest -q tests/test_imports.py` | **9 passed**, rc 0 (1 s). |
| `grep -rnE "undo_changes\|inverse" src/specir` | rc 1: sin implementación propia; solo aparecen las coincidencias del `bpmn-js` vendorizado. |
| `deskops graph missing --root .` | rc 0: «No missing graph references found.». |

Los dos bloqueos del intento 1 están resueltos: la prueba de identidad ya no es `xfail` estricto y las dos regresiones de D2-E pasan. `propose_changes` vuelve a rechazar con un error de herramienta que nombra «IR05 D2-E» y su descripción lo menciona; `test_blog_chain.py` y `test_domain_tools.py` quedan verdes sin tocar sus asserts (los 2 xfailed de `test_blog_chain.py` son los preexistentes de aristas, ajenos a este cambio).

## Hallazgo bloqueante: la Validación 1 no comprueba el store

La prueba `test_the_documents_and_the_store_have_the_same_content_after_the_undo` solo usa `content()`/`md_digest`, que recorren y hashean `*.md` bajo `.sldb`, `sldb`, `desk` y `undo`. Los índices de documentos del store son `.sldb/core/documents/**/*.yaml` y no se leen en ninguna parte; `set(content()) == set(before)` solo compara el conjunto de `.md`. La única comprobación del store tras un undo con éxito es `sldb rules check` / `sldb edges check`, que compara la salida de los checks, no el contenido. Por tanto, la prueba pasaría aunque el contenido del índice del store cambiara, y su nombre y docstring («and the store») y el resumen del ejecutor («mismo conjunto de archivos») sobredeclaran lo que comprueba.

La Validación 1 corregida por el coordinador pide comparar «el sha256 del texto sin bloque sldb, como `sldb/api/documents/content_hash.py` de sldb, igual antes y después, documento por documento, **y el store por el mismo criterio**». Falta esa mitad.

Comprobé aparte que el comportamiento es correcto: después de aplicar `content_batch("y")` y hacer `undo_changes(steps=1)`, el conjunto de entradas `.sldb/core/documents/**/*.yaml` y el `content_hash` de cada una son iguales antes y después; lo que cambia es `source_hash`, la procedencia `at`/`via` y hashes derivados (`model_hash`, `roster_hash`, `store_hash`), que el contrato de sldb permite. Lo que falta es que la prueba entregada lo afirme. Basta comparar por el mismo criterio de contenido las entradas del índice de documentos (conjunto de entradas y `content_hash` por documento), sin comparar bytes crudos, `source_hash`, procedencia ni hashes derivados.

## Nota menor (no bloqueante)

`md_digest` importa `strip_block` de `sldb.models.provenance_block`, un módulo interno de sldb. El pill `pill-guardrail-specir-solo-usa-la-api-pública-de-sldb` aplica también a `tests/`. Si no hay equivalente público, conviene usar el módulo bajo `sldb.api` (p. ej. `sldb.api.documents.content_hash`) o documentar la carencia y pedirla en el desk de sldb. No es el motivo del veredicto.

## Validación funcional del deshacer (lo que sí queda cubierto)

- Lote de creación, edición y arista: el contenido de los `.md` vuelve; `sldb rules check` y `edges check` salen rc 0. Pasa.
- Lote stale: `undo_changes` responde `applied: false`, `rejected: stale`, `document` y `written: false`, sin escribir; el lote sigue en la pila y se deshace tras revertir el cambio ajeno. Pasa.
- Niveles: nivel 0 no sirve herramientas de escritura ni `undo_changes`; nivel 1 rechaza un lote con `RuleDoc` y no deshace el lote de nivel 2; nivel 2 deshace el lote con `RuleDoc`. Pasa.
- Validadores de dominio: `undo_changes` aplica el lote inverso con `api.apply_batch` directo, así que `add_batch_validator` no corre sobre el deshacer; tras el undo, rules/edges y los validadores registrados sobre los documentos del lote no reportan error. Pasa y está documentado en la prueba.
- specIR no define `undo_changes` ni guarda lotes inversos. Pasa.

## Veredicto

**FALLA.** El deshacer funciona, los dos bloqueos del intento 1 están resueltos y todas las pruebas pedidas pasan, pero la Validación 1 tal como la fijó el coordinador no queda cubierta por la prueba entregada: se compara el contenido de los `.md`, no el del store. Hay que añadir la comparación del índice de documentos por `content_hash` (mismo criterio de contenido) y el conjunto de entradas; el comportamiento observado ya cumple ese criterio.
