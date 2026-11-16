# Brief del tester deskops-t-d802dff465a0 (.gitignore de IR; intento 1)

Eres el **tester independiente** de la tarea `task-ir-gitignore-ignora-egg-info-y-pycache` del desk IR, con la identidad `deskops-t-d802dff465a0` (rol tester, intento 1, contract_sha256 `74f2d1abb7345c9b8be8e854e7d8d604e126c4a35e100a28d6627f9d1480f59c`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-d802dff465a0/`.
- Usa `TMPDIR=/dev/shm`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash.

## Qué verificas
1. Lee la tarea con `deskops show task task-ir-gitignore-ignora-egg-info-y-pycache --root .` y su archivo en `desk/tasks/`. Corre por tu cuenta **cada** comando de su Validation y anota en `validation.log` la salida y el rc de cada uno.
2. Comprueba que el ejecutor solo cambió `.gitignore`. En el árbol hay cambios ajenos que no cuentan: `tests/conftest.py` y `tests/test_mcp_extension.py`, de una tarea bloqueada, y `.sldb/` y `runs/`, del registro de runs.
3. Comprueba que ningún archivo rastreado quedó ignorado con `git ls-files -ci --exclude-standard`, que no debe devolver nada, y que no se borró nada del disco: `src/specir.egg-info` sigue existiendo.
4. No hace falta la suite completa, porque el cambio no toca código. Corre una sola prueba de humo: `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py`.

Compara al final con el informe del ejecutor: `runs/subagents/deskops-e-d7008737b929/result-summary.md`.

## Qué dejas
- `validation.log`.
- `board.txt`: `deskops show board Board --root .`.
- `task.txt`: `deskops show task task-ir-gitignore-ignora-egg-info-y-pycache --root .`.
- `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación y un veredicto final.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
