# Brief del tester deskops-t-e9062210030f (IR13g, intento 1)

Eres el **tester independiente** de la tarea `task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee` del desk IR, con la identidad `deskops-t-e9062210030f` (rol tester, intento 1, contract_sha256 `0fea76a0464bf82489830560da4b0b667a7da1c5dc27dae0a11f0feaa8d9cc93`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-e9062210030f/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash.

## Qué verificas
1. Lee la tarea (`deskops show task` y su archivo en `desk/tasks/`) y las disposiciones aceptadas (preflight-2 y bundle-1). Corre **cada** comando de su Validation y de su Implementation Path. Anota la salida y el rc de cada uno en `validation.log`. Eso incluye:
   - el merge-base de 79d63ee;
   - el git grep de graph_ui: comprueba que las coincidencias que queden están solo en `desk/` y `runs/`, no en código ni en empaquetado;
   - `pytest -rxX tests/visual/test_notations_parity.py`;
   - el comprobador con las 5 rutas.
2. Revisa el diff de los dos documentos (`git diff docs/spec2viz/`) contra el Scope:
   - SV-H03 y SV-K22 cumplidas solo si sus pruebas pasan sin xfail y su único faltante era G4 de graph_ui;
   - SV-K18 sigue abierta;
   - el resumen de cumplidas y abiertas cuadra con un recuento tuyo de la tabla;
   - las filas no acreditadas del comprobador son exactamente las abiertas de la matriz;
   - el acta trae la fila de graph_ui resuelta con 79d63ee, c9b09f7 y la nota, el pendiente del ci.yml, G4 sin graph_ui, Lo que falta actualizado y el bloque nuevo de la corrida con el formato del de IR13f.

   Contrasta los SHAs y las cifras anotados con lo que obtienes tú. Que no afirme nada falso.
3. Fuera de `desk/`, `.sldb/` y `runs/` solo cambian los dos documentos. `tests/conftest.py` y `tests/test_mcp_extension.py` son cambios ajenos previos de una tarea bloqueada (`runs/subagents/deskops-e-068628774e48/diff.patch`); no los cuentes.
4. **Corre la suite completa una sola vez, bajo el lock**: `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes mira `free -g`: con menos de 8 GB disponibles, espera. Un rc 124 mientras esperas el lock no es un fallo: reencola. Si falla una prueba de digest «untouched» por escrituras de otro agente en el store real de deskops, compruébalo con los mtimes y `git -C ../deskops log`, y reencola una vez.

Compara al final con el informe del ejecutor, `runs/subagents/deskops-e-be491a5e3b00/result-summary.md`.

## Qué dejas
- `validation.log`.
- `board.txt`: `deskops show board Board --root .`.
- `task.txt`.
- `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación, las discrepancias y un veredicto final.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
