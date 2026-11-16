# Brief del tester deskops-t-63c09536450a (IR13f, intento 1)

Eres el **tester independiente** de la tarea `task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5` del desk IR, con la identidad `deskops-t-63c09536450a` (rol tester, intento 1, contract_sha256 `c15416e74e2e8a47fecc422897cc0b275fa0c760d3a47ee36a96a19d31d503ef`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-63c09536450a/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash.

## Qué verificas
1. Lee la tarea (`deskops show task` y su archivo en `desk/tasks/`) y corre **cada** comando de su Validation. Corre también el grep de `../pron/docs/spec2viz/build.py`, el merge-base de pron y los `ls ... | grep g5` de `../spec2viz/desk/{atoms,tasks}` del Implementation Path. Anota la salida y el rc de cada uno en `validation.log`.
2. Revisa el diff del acta (`git diff docs/spec2viz/acta-de-retiro.md`) contra los 4 puntos del Scope:
   - la fila de pron, resuelta con 4224186 y con lo que verificó su tester; contrasta lo que dice el acta con `../pron/desk/inbox` o con la nota citada;
   - la fila G5, con el estado «decidido; pendiente de ejecución en IR», el atom y la task.decision con sus ids exactos, y lo pendiente en IR;
   - «Lo que falta», sin pron en G4 y con la decisión en G5;
   - la corrida nueva del comprobador: córrelo tú y compara las filas abiertas, el número de dependencias y el rc.

   Que no afirme nada falso. La tarea `task-las-pruebas-de-mcp-dejan-de-federar-…` está bloqueada, con la nota a deskops 20261116-122447, y el acta debe decirlo así si lo menciona.
3. Fuera de `desk/`, `.sldb/` y `runs/` solo cambia el acta. `tests/conftest.py` y `tests/test_mcp_extension.py` son cambios ajenos previos de la tarea bloqueada (están en `runs/subagents/deskops-e-068628774e48/diff.patch`); no los cuentes.
4. **Corre la suite completa una sola vez, bajo el lock**: `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes mira `free -g`: con menos de 8 GB disponibles, espera. Un rc 124 mientras esperas el lock no es un fallo: reencola. Si falla `test_reading_through_every_tool_leaves_every_store_untouched` por cambios en el store real de deskops que hizo otro agente, compruébalo con los mtimes y `git -C ../deskops log`, y reencola una vez.

Compara al final con el informe del ejecutor, `runs/subagents/deskops-e-fa630485b00c/result-summary.md`.

## Qué dejas
- `validation.log`.
- `board.txt`: `deskops show board Board --root .`.
- `task.txt`.
- `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación, las discrepancias y un veredicto final.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
