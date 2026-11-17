# Brief del tester deskops-t-0e183e29ea34-a2 (copia del store de deskops en las pruebas MCP; intento 2)

Eres el **tester independiente** de la tarea `task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real` del desk IR, con la identidad `deskops-t-0e183e29ea34-a2` (rol tester, intento 2, contract_sha256 `d52071c726040e712846438c4b7888ed40f933ee8aae1283bc9658a09b8b7714`). Lee primero tu rol en `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`. Devuelves evidencia y nada más: **no implementas, no arreglas, no cierras y no commiteas.** Verifica todo por tu cuenta.

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de nada.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-0e183e29ea34-a2/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/`.
- No uses `pkill` ni `pgrep`, y no hagas `git add`, commit ni stash. **No escribas nunca en el store real de deskops.**

## Qué verificas
1. Lee la tarea, con sus precisiones (a)–(d), y las disposiciones aceptadas (preflight-5 y bundle-4; preflight-3 y bundle-2 en lo no cambiado). Corre **cada** comando de la Validation y anota su salida y su rc en `validation.log`.
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

Al final, compara con el informe del ejecutor: `runs/subagents/deskops-e-94a0788c3f5a-a2/result-summary.md`. Evalúa también su observación 2: `stores check` sobre la copia aislada da 2 store/missing, por RunDocs sin rastrear de deskops. Di si afecta al contrato.

## Qué dejas
- `validation.log`.
- `board.txt`: `deskops show board Board --root .`.
- `task.txt` y `git-status.txt`.
- `result-summary.md`, con PASS o FAIL por verificación, las discrepancias y un veredicto.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.

## Contexto del intento 2 (ciclo de corrección 1)
- El tester del intento 1 (`runs/subagents/deskops-t-af2c27434a91/result-summary.md`; léelo después de verificar) dio FAIL por D2: la sesión MCP leía el deskops real a través de symlinks a sldb y scion. La precisión (b) cambió: sin symlinks, se quitan los enlaces de la copia (o se copian los stores enlazados). La Validation agrega un **strace**: pasada la ventana de la copia, ningún proceso abre nada bajo `SLDB_1/deskops/`. **Repítelo tú**: es la verificación decisiva. Comprueba además que nada toca `SLDB_1/{sldb,pron,scion}/.sldb` ni `herramientas/deskops/.sldb`.
- Revisa la prueba nueva `test_no_store_linked_from_the_mounted_copy_leads_out_of_the_session_temp`: que compruebe algo real y que fallaría con los symlinks del intento 1. Revisa también el `stores declare --write` que el ejecutor agregó tras `stores remove`.
- **Fallo externo conocido de la suite:** 2 pruebas de `tests/visual/test_sync_generation_parity.py` fallan por una regresión de sldb 600b51a9: `component_spec_from_python` lee un `.js` minificado vendorizado. Ya está avisado a sldb (nota 20261116-213452). Si son exactamente esas 2, por esa causa, anótalas como ajenas. **Cualquier otro fallo cuenta.**
