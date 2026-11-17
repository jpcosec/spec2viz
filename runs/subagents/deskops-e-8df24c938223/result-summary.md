# IR04b — resultado (ejecutor deskops-e-8df24c938223): BLOQUEADO por hallazgo

## Entregado (sin commit)
`tests/test_mcp_undo.py` (nuevo; solo toca eso). Fixture: copia montada (`mount_copy`) + `python -m specir.install` + operación semilla escrita por una sesión nivel 1; luego sesiones `served(... --level N)` con la extensión de specIR. Casos:
1. nivel 1, lote crear DomainEntityDoc + editar DomainOperationDoc + arista `writes`; `undo_changes` y comparar digest (sha256 de todo) y .md, `rules check` / `edges check` iguales a antes y rc 0.
2. lote stale (cambio ajeno por `sldb.api.apply_batch`): applied false, rejected stale, document, written false, store intacto; el cambio ajeno se revierte desde OTRA sesión y el undo posterior pasa.
3. `steps=2` newest-first y pila vacía -> nothing_to_undo.
4. nivel 0: sin propose/apply/undo_changes; llamar undo_changes -> `unknown_tool`. **PASA**.
5. nivel 1: un lote con RuleDoc se rechaza en propose_changes (LevelError "needs write level 2"); no hay lote de reglas en la pila; nivel 2: el lote con RuleDoc se aplica y se deshace.
6. tras el undo, rules check/edges check; la extensión no registra `add_batch_validator`.
7. grep (f). **PASA**. Única coincidencia: `src/specir/visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js:2` (bpmn-js minificado de terceros, aparece "inverse"). No hay def, tool ni pila propias.

## Hallazgo (bloquea la Validation)
`apply_changes` por la sesión con la extensión de specIR aplica (`applied: true`), pero el `undo_changes` de sldb responde de inmediato:
`{'applied': False, 'rejected': 'nothing_to_undo', 'explanation': 'asked to undo 1 batch(es); this session has 0 applied batch(es) left to undo (the stack is per session and in memory)', 'written': False, 'undone': 0, 'remaining': 0}`
Igual con steps=2 y a nivel 2. Es decir, con la extensión montada no se puede deshacer nada.

Causa (leída en código, no corregida): `sldb/mcp/server.py::build_server` crea `WriteTools(store, level, actor, context=context)` y registra su `propose_changes`/`apply_changes`/`undo_changes`. `src/specir/mcp_extension.py::register` hace `writes = WriteTools(context.store_path, context.level, context.actor)` (sin `context`), quita `propose_changes` y `apply_changes` y registra los de ese segundo objeto. Cada `WriteTools` tiene su propio `UndoStack` (`sldb/mcp/write/tools.py`), así que `apply_changes` empuja al stack del segundo y `undo_changes` (del primero) mira uno vacío. Además, sin `context`, los `batch_validators` no corren en ese apply. Arreglo posible: que sldb exponga al extension el WriteTools/UndoStack de la sesión (o un hook para envolver propose_changes sin duplicar WriteTools), o que specIR reuse ese objeto; en cualquier caso lo primero es de sldb y lo segundo toca `mcp_extension.py`, que bundle-2 prohíbe tocar -> decisión del coordinador. No se escondió con xfail.

## Pendiente / a revisar
- Los 5 casos que aplican+deshacen fallan por este hallazgo; ítems de Validation 1, 2, 4(parcial: reglas tras undo) y 3 (nivel 2) no verificables hasta resolverlo.
- Tras la primera corrida corregí `foreign_edit` (el caso 2 fallaba además por mi formato de `apply_batch`: `payload must be an object`); ese cambio no se volvió a correr.
- `tests/test_mcp_extension.py` y `tests/test_imports.py` no corridos.
- `deskops graph missing --root .` rc 0.
- `.scion/settings.yaml` sin seguimiento ya existía antes.
