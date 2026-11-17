# Brief del ejecutor deskops-e-8df24c938223 (IR04b, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-8df24c938223` (rol executor, intento 1, contract_sha256 `fc0f36b0854708f310a829378049891e659bce5296de51342c27300d50559b4a`). Implementas solo el alcance, dejas la evidencia y te detienes. **No cierras, no commiteas, no avanzas el desk, no lanzas agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR` (`cd` ahí). Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-8df24c938223/`.
- `TMPDIR=/dev/shm`. Si `.venv/bin/python` no arranca en tu contenedor, usa un venv de trabajo en `/dev/shm` que reuse los site-packages de `.venv` (sldb editable desde `../sldb`, que ya trae `undo_changes`, d0ee07a3) y bórralo al terminar.

## La tarea
`task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas`. Lee `deskops show task … --root .`, su archivo en `desk/tasks/` (Implementation Path con las precisiones (a)–(g)) y las disposiciones aceptadas en `desk/reviews/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas/`: **preflight-3 y bundle-2** (son contrato). Lee también `../sldb/src/sldb/mcp/write/undo.py`, `../sldb/src/sldb/mcp/mutability.py` y `tests/conftest.py` (mount_copy, tree_digest, la sesión MCP).

Es una tarea de **verificación**: escribes pruebas en un módulo nuevo `tests/test_mcp_undo.py` contra el sldb mcp real con la extensión de specIR montada. Sin mocks. specIR no implementa el deshacer.

## Reglas
- Toca solo el módulo de prueba nuevo. `src/specir/mcp_extension.py` no se toca (bundle-2, punto 1).
- **Si sldb mcp no cumple algo de la Validation** (por ejemplo, con nivel 1 deshace un lote que tocó RelationTypeDoc o RuleDoc, o el deshacer deja reglas rotas), no lo arregles ni lo escondas con xfail: deja la prueba que lo muestra, anota el hallazgo con la salida exacta y detente con `EJECUTOR BLOQUEADO: hallazgo para sldb …`.
- No hagas `git add`, commit ni stash; no uses `pkill` ni `pgrep`; no edites `desk/` ni `.sldb/` del repo.
- Solo pruebas puntuales: el módulo nuevo, `tests/test_mcp_extension.py` y `tests/test_imports.py`. Antes de pytest, si `MemAvailable` es menor que 8 GB o `avg60` de `/proc/pressure/memory` es 10 o más, espera. Usa `flock /dev/shm/sldb1-tests.lock`.

## Qué dejas
`validation.log` (cada ítem de la Validation con su salida y rc), `diff.patch`, `git-status.txt`, `board.txt` (`cp desk/tasks/Board.md`), `task.txt` (`deskops show task …`) y `result-summary.md` (qué prueba cada caso, respuestas reales de undo_changes, coincidencias del grep una a una según (f), resultado de rules check y edges check tras el deshacer, hallazgos).

Al terminar responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
