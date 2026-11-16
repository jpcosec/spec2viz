# Brief del ejecutor deskops-e-be491a5e3b00 (IR13g, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-be491a5e3b00` (rol executor, intento 1, contract_sha256 `0fea76a0464bf82489830560da4b0b667a7da1c5dc27dae0a11f0feaa8d9cc93`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada, porque tu pane arrancó en el directorio padre.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-be491a5e3b00/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.

## La tarea
El contrato es la tarea `task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee`. Lee `deskops show task` y su archivo en `desk/tasks/`: Why, Scope, Implementation Path, Validation y Done When. Lee también sus pills y las disposiciones aceptadas en `desk/reviews/task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee/` (preflight-2 y bundle-1). Esas disposiciones fijan cómo resolver las ambigüedades:
- en la columna Dependencias de la fila de graph_ui del acta, sigue el precedente de pron;
- las cifras salen de recontar;
- las pruebas de SV-H03 son las que enumera la sección Acreditación (IR13).

## Reglas
- Solo puedes tocar `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`. `../UIs/graph_ui` y los demás repos son de solo lectura.
- **Si una verificación falla, detente y repórtalo.** Eso incluye el merge-base, el grep de graph_ui, las pruebas de SV-H03 o que las filas no acreditadas del comprobador no coincidan con las abiertas de la matriz. No marques nada como resuelto ni cumplido sin la evidencia.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- En el árbol hay cambios ajenos sin commitear en `tests/conftest.py` y `tests/test_mcp_extension.py`, de una tarea bloqueada. No los toques.
- Corre solo pruebas puntuales; no corras la suite completa.

## Validación
Corre cada comando de la Validation y del Implementation Path. Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff docs/spec2viz/`).
- `git-status.txt`.
- `result-summary.md`, con:
  - el estado nuevo de SV-H03, SV-K18 y SV-K22, y su motivo;
  - el resumen de cumplidas y abiertas;
  - qué cambió en el acta;
  - la corrida del comprobador: filas abiertas, dependencias por repo y rc;
  - lo que queda pendiente.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
