# Brief del tester deskops-t-fb41c88d0a4a (IR13h, intento 1)

Eres el **tester independiente** de la tarea `task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4` del desk IR, con la identidad `deskops-t-fb41c88d0a4a` (rol tester, intento 1, contract_sha256 `28509da07e3fb092fe84c5d16be68442226270fc226e177e71f8a2c37ace80a1`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-fb41c88d0a4a/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash.

## Qué verificas
1. Lee la tarea (`deskops show task` y su archivo en `desk/tasks/`) y las disposiciones aceptadas (preflight-2 y bundle-1). Corre **cada** comando de su Validation y de su Implementation Path, con la salida y el rc de cada uno en `validation.log`:
   - los merge-base de deskops contra `origin/main` (haz `git -C ../deskops fetch -q origin` antes);
   - el grep del store_index de deskops: comprueba que lo que quede no sea un enlace de store a spec2viz;
   - el comprobador con las 5 rutas;
   - pytest de la matriz y el gate;
   - graph missing.
2. Revisa el diff (`git diff docs/spec2viz/`) contra el Scope. Comprueba:
   - la fila de deskops del acta: resuelta, con los 3 pares de commits y la celda Dependencias con la forma de pron y graph_ui;
   - que G4 del acta y de la matriz y Lo que falta no nombren a graph_ui, deskops ni pron como pendientes;
   - el bloque nuevo de la corrida, con el formato del de IR13g;
   - que el reemplazo del bloque «Salida del comprobador» coincida línea a línea con tu corrida;
   - que las cifras y los SHAs anotados coincidan con lo que obtienes tú;
   - que el acta no afirme nada falso.
3. Fuera de `desk/`, `.sldb/` y `runs/` solo cambian los dos documentos.
4. **Corre la suite completa una vez, bajo el lock:** `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`.
   - Antes, mira `free -g`: con menos de 8 GB disponibles, espera.
   - Un rc 124 mientras esperas el lock no es un fallo de las pruebas.
   - **Fragilidad conocida:** `test_reading_through_every_tool_leaves_every_store_untouched` digiere el store real de deskops. Si falla por escrituras de un agente de deskops durante la corrida, compruébalo con mtimes, `git -C ../deskops log` y `git -C ../deskops status`, y reencola **una** vez. Ya hay una tarea abierta para corregirlo.

Al final, compara con el informe del ejecutor: `runs/subagents/deskops-e-5d20e77cfc47/result-summary.md`.

## Qué dejas
- `validation.log`.
- `board.txt`, con `deskops show board Board --root .`.
- `task.txt` y `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación, las discrepancias y un veredicto.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
