# Brief del ejecutor deskops-e-674fcb14989b-a2 (IR04b, intento 2)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-674fcb14989b-a2` (rol executor, intento 2, contract_sha256 `a36c00d8bbc113fa345c761fe562926ee7a5477109aef5df6a7d934c67cd8891`). Implementas solo el alcance, dejas la evidencia y te detienes. **No cierras, no commiteas, no avanzas el desk, no lanzas agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR` (`cd` ahí). Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-674fcb14989b-a2/`.
- `TMPDIR=/dev/shm`. Si `.venv/bin/python` no arranca en tu contenedor, usa un venv de trabajo en `/dev/shm` que reuse los site-packages de `.venv` (sldb editable desde `../sldb`) y bórralo al terminar.

## La tarea
`task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas`. Lee `deskops show task … --root .`, su archivo en `desk/tasks/` (Implementation Path, precisiones (a)–(g); la (e) cambió) y las disposiciones aceptadas en `desk/reviews/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas/`: **preflight-4 y bundle-3** (son contrato; sustituyen a preflight-3 y bundle-2).

## Qué pasó en el intento 1
Lee `runs/subagents/deskops-e-8df24c938223/result-summary.md`. El ejecutor anterior escribió `tests/test_mcp_undo.py` (está en el árbol, sin commit; parte de él). Hallazgo: `src/specir/mcp_extension.py::register` crea un segundo `WriteTools` de sldb sin `context` y reemplaza `propose_changes`/`apply_changes`; ese objeto tiene su propia `UndoStack`, así que el `undo_changes` de la sesión responde `nothing_to_undo`. La causa es de specIR, no de sldb.

## Qué haces
1. **Corrige la extensión** (`src/specir/mcp_extension.py`): no crea `WriteTools`, no quita ni registra `propose_changes`/`apply_changes`. Registra la regla IR05 D2-E (no escribir `verificacion: verificado`) con `context.add_batch_validator`, siguiendo el contrato `BatchValidator` de `../sldb/src/sldb/mcp/extension.py` (finding `{code, level: "error", what, subject}`). El validador recibe `Change` tipados en propose y `BatchChange` (de la propuesta) en apply; reconoce ambos. Lee `../sldb/src/sldb/mcp/write/tools.py` y `context.py`.
2. Ajusta `tests/test_mcp_extension.py` a la nueva forma del rechazo (`domain` de sldb) **sin debilitar**: siguen cubiertos el rechazo en propose y en apply y que no se escribe nada.
3. Termina `tests/test_mcp_undo.py` (incluye el arreglo de `foreign_edit` que no se volvió a correr) y córrelo. El cambio ajeno se hace y se revierte con `sldb.api.apply_batch` fuera de la sesión MCP. Tras cada undo: `sldb rules check` y `sldb edges check` rc 0, y corre los validadores registrados sobre los documentos del lote; si alguno da error, es hallazgo para sldb.

## Reglas
- Toca solo `src/specir/mcp_extension.py`, `tests/test_mcp_extension.py`, `tests/test_mcp_undo.py` (y `tests/conftest.py` solo si hace falta un fixture).
- **Si sldb mcp no cumple algo de la Validation** (p. ej. nivel 1 deshace un lote que tocó RelationTypeDoc o RuleDoc, o el deshacer deja reglas rotas), no lo arregles ni lo escondas con xfail: deja la prueba que lo muestra, anota la salida exacta y detente con `EJECUTOR BLOQUEADO: hallazgo para sldb …`. No toques `../sldb`.
- No hagas `git add`, commit ni stash; no uses `pkill` ni `pgrep`; no edites `desk/` ni `.sldb/` del repo.
- Pruebas: `tests/test_mcp_undo.py`, `tests/test_mcp_extension.py`, `tests/test_imports.py`, y cualquier otro módulo que importe `specir.mcp_extension` (búscalos con grep). Antes de pytest, si `MemAvailable` es menor que 8 GB o `avg60` de `/proc/pressure/memory` es 10 o más, espera. Usa `flock /dev/shm/sldb1-tests.lock`. La suite completa la corre el tester.

## Qué dejas
`validation.log` (cada ítem de la Validation con su salida y rc, más el grep (f) con cada coincidencia clasificada), `diff.patch` (incluye el archivo nuevo), `git-status.txt`, `board.txt` (`cp desk/tasks/Board.md`), `task.txt` (`deskops show task …`) y `result-summary.md` (qué cambió en la extensión, qué prueba cada caso, respuestas reales de undo_changes, rules/edges check tras el deshacer, qué hace undo con los validadores de dominio, hallazgos).

Al terminar responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
