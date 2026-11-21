FALLA

# Resultado del tester (IR04b, cierre: identidad por contenido y sin imports internos)

- task: `task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import`
- commit del ejecutor: `33846f54689e9db0d56909e6359034ca384dd086` — *IR04b cierre: la prueba de identidad compara también el store por contenido; md_digest sin módulos internos de sldb*
- archivos del commit: `tests/test_mcp_undo.py` (28 inserciones, 5 borrados).
- entorno: worktree limpio en `33846f5` (`/workspace/ir04b-clean2`, detached HEAD), `PYTHONPATH=/workspace/ir04b-clean2/src`, `TMPDIR=/tmp`, `.venv/bin/python` del repo. No se tocó el commit; el worktree quedó limpio al terminar.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `pytest -q tests/test_mcp_undo.py` | **7 passed, 1 failed**, rc 1 (193 s), sin xfail. |
| `pytest -q tests/models/test_blog_chain.py` | **7 passed, 2 xfailed**, rc 0 (13,8 s). |
| `pytest -q tests/models/test_domain_tools.py` | **5 passed**, rc 0 (11,8 s). |
| `pytest -q tests/test_mcp_extension.py` | **11 passed**, rc 0 (108,8 s). |
| `pytest -q tests/test_imports.py` (guardrail de imports de `src/specir`) | **9 passed**, rc 0 (0,75 s). |
| `grep` de imports internos en `tests/test_mcp_undo.py` | quedan `from sldb.mcp.changes import BatchChange`, `from sldb.mcp.context import ServerContext` y `from sldb.mcp.server import build_server` (líneas 267-269). |
| `grep` de `xfail`/`skip` en `tests/test_mcp_undo.py` | sin coincidencias. |

## Fallo bloqueante: la comparación del store no es estable y rompe el test stale

`tests/test_mcp_undo.py::test_a_stale_batch_is_refused_without_writing_and_undone_once_the_foreign_change_is_reverted` falla en `assert content() == mds` (línea 208):

```
Omitting 509 identical items, use -vv to show
Left contains 452 more items:
{'store:AtomDoc/...': '...', 'store:ReviewDoc/...': '...', ...}
```

No es que el deshacer haya cambiado el contenido: los 509 elementos comunes (456 `.md` + las entradas de store presentes en ambas instantáneas) tienen exactamente el mismo hash. Lo que cambia es **el conjunto de documentos que devuelve `api.load_runtime_documents`**:

- al empezar el test, `load_runtime_documents(root/.sldb)` devuelve solo **53 documentos**: `RelationTypeDoc` (27), `RuleDoc` (21), `RelationDoc` (4) y `DomainOperationDoc` (1);
- tras la escritura in-process de `foreign_edit` (`api.apply_batch`) devuelve **506 documentos**, y `content()` incorpora 452/453 claves `store:...` nuevas.

La causa es que `sldb.api.load_runtime_documents` recorre los modelos del `store_index` y **omite en silencio** los que no resuelven (`_resolve_model_type` devuelve `None`). En la copia montada, los modelos heredados de deskops tienen `model_ref: deskops.models:...` y no resuelven desde el root del proyecto montado al inicio; tras la escritura in-process pasan a resolverse y aparecen los 506. Por eso el resultado de `content()` depende del estado interno de resolución del proceso, no solo del contenido del store.

Reproducciones:
- haciendo `TMPDIR=/tmp ... pytest -q tests/test_mcp_undo.py -k stale` en el mismo worktree limpio: **1 failed, 7 deselected**;
- la prueba de identidad `test_the_documents_and_the_store_have_the_same_content_after_the_undo` sí pasa en la misma ejecución: compara bien `.md` y los hashes de store que ve, pero el helper `content()` que ahora incluye store también se usa en el test stale, que es donde revienta.

Arreglo esperado: comparar el store por el `content_hash` de cada entrada trackeada (conjunto de entradas + `content_hash` por documento, sin bytes crudos ni `source_hash`/procedencia), como pidió el tester anterior, o forzar una lectura estable de los 506 documentos antes de tomar la instantánea. No se debe comparar el conjunto que devuelve `load_runtime_documents` tal cual. No hay ningún fallo real del deshacer que corregir en `src/specir/`.

## Segundo hallazgo: imports internos de sldb en el archivo

El objetivo concreto de `md_digest` sí está cumplido: ya no importa `sldb.models.provenance_block.strip_block`; quita el bloque `sldb` con `yaml` local y usa `sldb.api` para el store. Pero el Done When dice literalmente «no hay imports de módulos internos de sldb en `tests/test_mcp_undo.py`» y el archivo conserva los tres imports de `sldb.mcp.*` de las líneas 267-269 (preexistentes, usados por `test_the_store_after_an_undo_passes_the_checks_and_the_registered_domain_validators`). `sldb.api` no exporta `build_server`, `ServerContext` ni `BatchChange`, así que eliminarlos exige una API pública de sldb o documentar la carencia; no es un cambio trivial. Si el criterio se refiere solo al helper de digest, este punto queda como nota; si se lee literalmente, también bloquea.

## Veredicto

**FALLA.** El commit añade la comparación del store y elimina el import de `sldb.models`, pero la validación pedida no pasa: `tests/test_mcp_undo.py` tiene 1 test fallido porque el conjunto de documentos que `load_runtime_documents` devuelve antes y después de una escritura in-process no es estable. Los otros tres archivos pedidos pasan (7+2 xfailed, 5 y 11). No se reveló un fallo del deshacer: los hashes de los documentos comunes son idénticos. Además, el archivo sigue importando módulos internos `sldb.mcp.*`, contrario al Done When literal.
