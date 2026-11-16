# Brief del tester deskops-t-79b9a3c32e0f (federación de las pruebas MCP, G5 opción A; intento 1)

Eres el **tester independiente** de una tarea del desk IR, con la identidad `deskops-t-79b9a3c32e0f` (rol tester, intento 1, contract_sha256 `39d7d97e36dab7cdddf9d623acf2b0f270796e43032f36936d07535324971908`). Tu rol es el de `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`: léelo primero. Devuelves evidencia. **No implementas, no arreglas, no ruteas, no cierras y no commiteas.** Verifica todo por tu cuenta.

## Dónde
- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí, porque tu pane arrancó en el directorio padre.
- Tu run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-79b9a3c32e0f/`.
- Usa siempre `TMPDIR=/dev/shm` y `.venv/bin/python`.

## Qué pruebas
La tarea es `task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a`. Lee su archivo en `desk/tasks/` (Scope, Implementation Path con las precisiones a–d, Validation y Done When) y las disposiciones aceptadas en `desk/reviews/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/`: preflight-3 y bundle-3.

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
