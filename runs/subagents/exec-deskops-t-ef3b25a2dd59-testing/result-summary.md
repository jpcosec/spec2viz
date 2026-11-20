FALLA

# Resultado del tester (IR04b: deshacer por MCP sobre el lote inverso de sldb)

- task: `task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas`
- commit del ejecutor: `1be6fc1bd16c4dd4bd620d42810fa6d6b3f09d34` — *IR04b: undo por MCP sobre el lote inverso de sldb; IR05 D2-E como add_batch_validator*
- archivos del commit: `src/specir/mcp_extension.py`, `tests/test_mcp_extension.py`, `tests/test_mcp_undo.py`.
- Entorno: `.venv/bin/python` del repo, `TMPDIR=/tmp`, desde la raíz de IR.

## Comprobaciones del encargo

| Comprobación | Resultado |
|---|---|
| `pytest -q tests/test_mcp_undo.py` | **7 passed, 1 xfailed**, rc 0 (187 s). |
| `pytest -q tests/test_mcp_extension.py` | **11 passed**, rc 0 (110 s). |
| `grep -rnE "undo_changes\|inverse" src/specir` | rc 1: sin coincidencias; specIR no define el deshacer ni guarda lotes. |
| `deskops graph missing --root .` | rc 0: «No missing graph references found.». |

Las pruebas propias del deshacer pasan, salvo la de identidad byte a byte, que está marcada `xfail(strict=True)`. Su motivo es real: tras `undo_changes` el contenido vuelve, pero sldb re-sella `sldb.at`/`sldb.via` del documento editado y cambian los hashes derivados de `.sldb/`. El contrato documentado de sldb (`docs/architecture/mcp.md` y nota de inbox 20261118-211934) es «mismo contenido salvo procedencia» y pide relajar la validación de specIR a contenido; la tarea, sin embargo, sigue exigiendo sha256 idéntico. El propio resultado del ejecutor reconoce que la Validation 1 queda «only partly met».

## Regresiones en pruebas existentes (bloqueantes)

El cambio de la extensión rompe dos módulos que ya existían y que ejercitan `specir.mcp_extension`:

| Módulo | Resultado |
|---|---|
| `tests/models/test_blog_chain.py` | **1 failed, 6 passed, 2 xfailed**, rc 1. Falla `test_an_agent_does_not_verify_through_the_mcp`: espera que `propose_changes` sea un error de herramienta con «IR05 D2-E»; ahora devuelve el rechazo `domain` estructurado (`applied: false`, `rejected: domain`, `written: false`). |
| `tests/models/test_domain_tools.py` | **1 failed, 4 passed**, rc 1. Falla `test_the_write_tools_come_with_the_extension_from_level_1`: espera «IR05 D2-E» en la descripción de `propose_changes`; la extensión ya no reemplaza la tool, así que la descripción es la de sldb. |

No son fallos ajenos al alcance: los dos esperaban la forma anterior del rechazo y el commit la cambia. Hay que ajustarlos al rechazo `domain` sin debilitar lo que comprueban (y, en `test_domain_tools`, comprobar el efecto del validador en vez del texto de la descripción) o, si el coordinador lo decide, declarar explícitamente que otra tarea los corrige antes de integrar.

`tests/test_imports.py` (9 passed) y `tests/visual/test_sync_generation_parity.py` (22 passed) sí quedan en verde.

## Validación funcional del deshacer

- Lote de creación, edición y arista: el contenido de los `.md` vuelve y `sldb rules check`/`edges check` salen rc 0; la copia no queda byte-idéntica solo por el re-sellado de procedencia (xfail anterior).
- Lote stale: `undo_changes` responde `applied: false`, `rejected: stale`, `document` y `written: false` sin escribir; el lote sigue en la pila y se deshace tras revertir el cambio ajeno. Pasa.
- Niveles: nivel 0 no sirve herramientas de escritura ni `undo_changes`; nivel 1 rechaza un lote con `RuleDoc` y no deshace el lote de nivel 2; nivel 2 deshace el lote con `RuleDoc`. Pasa.
- Validadores de dominio: `undo_changes` aplica el lote inverso con `api.apply_batch` directo, así que `add_batch_validator` no corre sobre el deshacer; tras el undo, rules/edges y los validadores registrados sobre los documentos del lote no reportan error. Pasa.
- specIR no implementa `undo_changes` ni guarda lotes inversos. Pasa.

## Veredicto

**FALLA.** El deshacer funciona y las pruebas nuevas lo cubren, pero (1) la Validation 1 escrita (sha256 idéntico de los `.md` y del store) no se cumple y queda como `xfail` estricto, y (2) el commit deja en rojo dos pruebas existentes de `tests/models/` que fueron afectadas por el cambio de rechazo y de descripción de las write tools. Antes de cerrar hay que ajustar esas pruebas (o dejar por escrito que otra tarea las corrige) y decidir si la validación de identidad se relaja a «mismo contenido salvo procedencia», como pide sldb.
