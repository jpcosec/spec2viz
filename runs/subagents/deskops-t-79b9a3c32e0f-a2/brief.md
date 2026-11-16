# Brief del tester deskops-t-79b9a3c32e0f-a2 (federación de las pruebas MCP, G5 opción A; intento 2)

Eres el **tester independiente** de una tarea del desk IR, con la identidad `deskops-t-79b9a3c32e0f-a2` (rol tester, intento 2, contract_sha256 `39d7d97e36dab7cdddf9d623acf2b0f270796e43032f36936d07535324971908`). Tu rol es el de `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`: léelo primero. Devuelves evidencia. **No implementas, no arreglas, no ruteas, no cierras y no commiteas.** Verifica todo por tu cuenta.

## Dónde
- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí, porque tu pane arrancó en el directorio padre.
- Tu run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-79b9a3c32e0f-a2/`.
- Usa siempre `TMPDIR=/dev/shm` y `.venv/bin/python`.

## Qué pruebas
La tarea es `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a`. Lee su archivo en `desk/tasks/` (Scope, Implementation Path con las precisiones a–d, Validation y Done When) y las disposiciones aceptadas en `desk/reviews/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/`: preflight-4 y bundle-5 (vigentes; preflight-3 y bundle-3 fijan las precisiones).

El trabajo está **sin commitear**: `git diff tests/conftest.py tests/test_mcp_extension.py`. El informe del ejecutor está en `runs/subagents/deskops-e-068628774e48/result-summary.md`. Léelo solo después de verificar por tu cuenta, para comparar.

## Verificaciones (todas, con su salida y rc en tu validation.log)
1. Los greps y la prueba puntual de la Validation: `tests/test_mcp_extension.py` con `-rs`, sin skipped, y `test_a_spec_of_the_linked_spec2viz_store_is_read_through_the_server` debe pasar. Corre también `tests/visual/test_visual_projections.py` y `tests/models/test_blog_chain.py`.
2. **La suite completa, una sola vez, bajo el lock**: `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes mira `free -g`; con menos de 8 GB disponibles, espera y vuelve a mirar. Un rc 124 mientras esperas el lock no es un fallo de las pruebas: reencola la corrida.
3. `deskops graph missing --root .`, que debe dar rc 0.
4. Comprueba el contrato a mano:
   - Ninguna prueba lee ni enlaza el store real `../spec2viz/.sldb`. Durante la corrida de `test_mcp_extension.py`, verifica que `../spec2viz/.sldb` no se lee: por ejemplo, compara su mtime y su digest antes y después, o usa strace si lo tienes.
   - El store temporal se construye con la API pública (`init_store` y `SpecSync`), sin mocks, desde la fixture real.
   - Las precisiones (a)–(d) se cumplen, incluida la cobertura del digest de «untouched».
   - El cambio en la fuente del payload esperado (`extract_document_payload` en vez del front matter crudo) **no relaja** ninguna aserción sobre la respuesta del servidor y está autorizado por el Implementation Path y por preflight-3. Juzga si la prueba sigue probando lo que debe.
   - Fuera de `desk/`, `.sldb/` y `runs/` solo cambian los 2 archivos.

## Qué dejas
- `validation.log`.
- `board.txt`: `deskops show board Board --root .`.
- `task.txt`: `deskops show task <id> --root .`.
- `git-status.txt` y `graph.txt`.
- `result-summary.md`, con:
  - PASS o FAIL por verificación y su evidencia;
  - las discrepancias con el ejecutor;
  - un veredicto final.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.

## Contexto del intento 2
- El tester del intento 1 (`runs/subagents/deskops-t-79b9a3c32e0f/result-summary.md`, léelo después de verificar) dio FAIL solo en 4a. La sesión `sldb mcp` leía `../spec2viz/.sldb` de forma transitiva porque `deskops/.sldb` lo enlazaba. Por decisión de JP (opción b), deskops quitó ese enlace en 421d6a27 (closeout 74ffdb63, en origin) y el espejo de IR está cerrado (f064795). **Repite la medición con strace: ahora tiene que dar 0 aperturas bajo `../spec2viz`.** Comprueba también que `../deskops/.sldb/core/store_index.yaml` ya no enlaza spec2viz.
- El código no cambió desde el intento 1. Comprueba que `git diff tests/conftest.py tests/test_mcp_extension.py` coincide con `runs/subagents/deskops-e-068628774e48/diff.patch`.
- **Fragilidad conocida.** `test_reading_through_every_tool_leaves_every_store_untouched` digiere el store real de deskops, así que falla si un agente de deskops escribe mientras corre la suite. Hay una tarea aparte para arreglarlo. Si falla así, compruébalo con mtimes, `git -C ../deskops log` y `git -C ../deskops status`, y reencola la suite **una** vez. Si vuelve a fallar por lo mismo, repórtalo con esa evidencia; no lo cuentes como fallo de la tarea solo si lo demuestras.
