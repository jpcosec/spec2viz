# Brief del ejecutor deskops-e-473333353dce (copia del store de deskops en las pruebas MCP; intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-473333353dce` (rol executor, intento 1, contract_sha256 `081661cf8fd8d00b4acb5c9efa6bc71363ea8be581f28c26d99686c3076dc362`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-473333353dce/`.
- Usa `TMPDIR=/dev/shm` y el `.venv` de IR.

## La tarea
El contrato es `task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real`. Lee `deskops show task` y su archivo en `desk/tasks/`, con las precisiones (preflight-1) de la (a) a la (d), sus pills y las disposiciones aceptadas en `desk/reviews/task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real/` (preflight-3 y bundle-2). Esas disposiciones resuelven las dudas así:
- La caché es la constante `CACHE` (`.sldb_cache`). Los archivos sin rastrear no entran.
- `<deskops>` es `WORKSPACE / "deskops"`.
- La lista de `git ls-files` se toma una sola vez, al hacer la copia. Después todo se lee de la copia.
- «Rompe» quiere decir que `sldb stores add` o `check` sobre la copia falla, o que la sesión MCP no resuelve un store enlazado.
- El grep acepta coincidencias solo dentro de `build_deskops_copy`.

Lee primero `tests/conftest.py` y `tests/test_mcp_extension.py` completos. La tarea anterior, cerrada en b16aab7, introdujo `build_spec_store`, `spec_store` y `spec_store_digest`. Sigue ese patrón.

## Reglas
- Fuera de `desk/`, `.sldb/` y `runs/`, solo puedes tocar `tests/conftest.py` y `tests/test_mcp_extension.py`.
- `../deskops`, `../sldb`, `../pron` y `../scion` son de **solo lectura**. **No escribas nunca en el store real de deskops.**
- Sin mocks ni datos fabricados. Las aserciones de la prueba de untouched no se relajan.
- Si la copia rompe la resolución de los enlaces, detente y anótalo como bloqueo.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- Corre solo pruebas puntuales; no corras la suite completa.

## Validación
Corre los comandos de la Validation, salvo la suite completa, que es del tester. Corre también uno por uno los archivos que usan los fixtures que cambies (`grep -lE 'FEDERATED|federated_digest|mount_copy|store_copy|deskops_copy' -r tests`). Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff tests/conftest.py tests/test_mcp_extension.py`).
- `git-status.txt` y `diff-stat.txt`.
- `result-summary.md`, con:
  - los cambios y cómo cumplen (a)–(d);
  - los resultados;
  - lo pendiente o bloqueado.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
