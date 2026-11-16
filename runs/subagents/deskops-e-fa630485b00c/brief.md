# Brief del ejecutor deskops-e-fa630485b00c (IR13f, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-fa630485b00c` (rol executor, intento 1, contract_sha256 `c15416e74e2e8a47fecc422897cc0b275fa0c760d3a47ee36a96a19d31d503ef`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada, porque tu pane arrancó en el directorio padre.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-fa630485b00c/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.

## La tarea
El contrato es la tarea `task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5`. Lee `deskops show task <id> --root .` y su archivo en `desk/tasks/`: Why, Scope, Implementation Path, Validation y Done When. Lee también sus pills y las disposiciones en `desk/reviews/task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5/` (preflight-1 y bundle-1).

## Reglas
- El único archivo que puedes tocar es `docs/spec2viz/acta-de-retiro.md`. `../pron`, `../spec2viz` y los demás repos son de solo lectura.
- Si la verificación de pron falla (el grep o el merge-base), no marques la fila como resuelta: anota lo que encontraste y repórtalo.
- Contexto para la fila G5: la tarea `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a` está **bloqueada**. El tester encontró que las pruebas MCP todavía leen `../spec2viz/.sldb` de forma transitiva, porque `deskops/.sldb` enlaza spec2viz. Se pidió a deskops con la nota de inbox 20261116-122447. Si lo anotas en lo pendiente de G5, cítalo así, sin inventar más. Ese pendiente sigue siendo de IR.
- IR13e (b159abd) ya actualizó el acta con su corrida del comprobador. Agrega una corrida nueva, conservando el formato de las anteriores.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- En el árbol hay cambios ajenos sin commitear en `tests/conftest.py` y `tests/test_mcp_extension.py`, de la tarea bloqueada. No los toques.
- Corre solo pruebas puntuales; no corras la suite completa.

## Validación
Corre cada comando de la Validation de la tarea, junto con el grep y el merge-base de pron y los `ls` de spec2viz del Implementation Path. Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff docs/spec2viz/acta-de-retiro.md`).
- `git-status.txt`.
- `result-summary.md`: qué cambiaste en cada uno de los 4 puntos del scope, la salida resumida del comprobador (filas abiertas, número de dependencias y rc) y lo que quede pendiente.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
