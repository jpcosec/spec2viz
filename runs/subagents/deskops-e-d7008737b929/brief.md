# Brief del ejecutor deskops-e-d7008737b929 (.gitignore de IR; intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-d7008737b929` (rol executor, intento 1, contract_sha256 `74f2d1abb7345c9b8be8e854e7d8d604e126c4a35e100a28d6627f9d1480f59c`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas y no avanzas el desk.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-d7008737b929/`.
- Usa `TMPDIR=/dev/shm`.

## La tarea
El contrato es la tarea `task-ir-gitignore-ignora-egg-info-y-pycache`. Lee `deskops show task <id> --root .`, su archivo `desk/tasks/task-ir-gitignore-ignora-egg-info-y-pycache.md` y las disposiciones en `desk/reviews/task-ir-gitignore-ignora-egg-info-y-pycache/`: preflight-1 y bundle-1.

## Reglas
- El único archivo que puedes tocar es `.gitignore`. No borres los `__pycache__` ni el egg-info: solo hay que ignorarlos.
- No hagas `git add`, `commit`, `stash` ni `git add -A`. No uses `pkill` ni `pgrep`. No edites `desk/` ni `.sldb/` a mano.
- En el árbol hay cambios ajenos sin commitear en `tests/conftest.py` y `tests/test_mcp_extension.py`, de una tarea bloqueada. No los toques.

## Validación
Corre cada comando de la Validation de la tarea y deja en `validation.log` la salida y el rc de cada uno.

## Qué dejas
- `validation.log` y `diff.patch` (`git diff .gitignore`).
- `git-status.txt`.
- `result-summary.md`.

Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta>` o `EJECUTOR BLOQUEADO: <motivo>`.
