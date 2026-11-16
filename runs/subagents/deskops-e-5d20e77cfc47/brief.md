# Brief del ejecutor deskops-e-5d20e77cfc47 (IR13h, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-5d20e77cfc47` (rol executor, intento 1, contract_sha256 `28509da07e3fb092fe84c5d16be68442226270fc226e177e71f8a2c37ace80a1`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada, porque tu pane arrancó en el directorio padre.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-5d20e77cfc47/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.

## La tarea
El contrato es la tarea `task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4`. Lee `deskops show task` y su archivo en `desk/tasks/`: Why, Scope, Implementation Path, Validation y Done When. Lee también sus pills y las disposiciones aceptadas en `desk/reviews/task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4/` (preflight-2 y bundle-1). Esas disposiciones fijan cómo resolver las ambigüedades. La celda Dependencias sigue la forma de las filas de pron y graph_ui. G4 refleja nombres y recuentos de la corrida nueva. Todos los comandos se corren desde la raíz de IR.

## Reglas
- Solo puedes tocar `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`. `../deskops` y los demás repos son de solo lectura.
- **Si una verificación falla, detente y repórtalo.** Eso incluye los merge-base de deskops, el grep de su store_index o que las filas no acreditadas del comprobador no coincidan con las abiertas de la matriz. No marques nada como resuelto ni cumplido sin la evidencia.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- Corre solo pruebas puntuales; no corras la suite completa.

## Validación
Corre cada comando de la Validation y del Implementation Path. Deja la salida y el rc de cada uno en `validation.log`.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff docs/spec2viz/`).
- `git-status.txt`.
- `result-summary.md`, con qué cambió en el acta (la fila de deskops, G4 y Lo que falta) y en la línea de G4 de la matriz, la corrida del comprobador (filas abiertas, dependencias por repo, rc y HEADs) y lo pendiente.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
