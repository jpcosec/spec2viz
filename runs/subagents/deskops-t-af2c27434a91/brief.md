# Brief del tester deskops-t-af2c27434a91 (copia del store de deskops en las pruebas MCP; intento 1)

Eres el **tester independiente** de la tarea `task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real` del desk IR, con la identidad `deskops-t-af2c27434a91` (rol tester, intento 1, contract_sha256 `081661cf8fd8d00b4acb5c9efa6bc71363ea8be581f28c26d99686c3076dc362`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-af2c27434a91/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash. **No escribas nunca en el store real de deskops.**

## Qué verificas
1. Lee la tarea, con sus precisiones (a)–(d), y las disposiciones aceptadas (preflight-3 y bundle-2). Corre **cada** comando de la Validation y anota su salida y su rc en `validation.log`.
2. Revisa `git diff tests/conftest.py tests/test_mcp_extension.py` contra (a)–(d). En particular:
   - la copia se hace una sola vez, en un fixture de sesión, sin la caché ni archivos sin rastrear;
   - los symlinks sldb, pron y scion existen;
   - no queda ninguna ruta real de deskops fuera de `build_deskops_copy`;
   - las aserciones de `test_reading_through_every_tool_leaves_every_store_untouched` no se relajaron (compáralas con `git show HEAD:tests/test_mcp_extension.py`);
   - la prueba nueva `test_the_deskops_store_linked_is_the_session_copy` comprueba algo real;
   - no hay mocks.
3. **Comprueba que la cura funciona:** demuestra que una escritura en el store real de deskops durante la prueba ya no la tumba, **sin escribir en deskops**. Por ejemplo, con strace sobre `tests/test_mcp_extension.py`, verifica que el digest y la sesión MCP no abren archivos bajo `SLDB_1/deskops/` fuera del momento de la copia, o razónalo con el código y una traza.
4. Fuera de `desk/`, `.sldb/` y `runs/` solo cambian los 2 archivos.
5. **Suite completa una vez, bajo el lock:** `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes mira `free -g`; con menos de 8 GB disponibles, espera. Un rc 124 mientras esperas el lock no es un fallo de las pruebas.

Al final, compara con el informe del ejecutor: `runs/subagents/deskops-e-473333353dce/result-summary.md`. Evalúa también su observación 2: `stores check` sobre la copia aislada da 2 store/missing, por RunDocs sin rastrear de deskops. Di si afecta al contrato.

## Qué dejas
- `validation.log`.
- `board.txt`: `deskops show board Board --root .`.
- `task.txt` y `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación, las discrepancias y un veredicto.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
