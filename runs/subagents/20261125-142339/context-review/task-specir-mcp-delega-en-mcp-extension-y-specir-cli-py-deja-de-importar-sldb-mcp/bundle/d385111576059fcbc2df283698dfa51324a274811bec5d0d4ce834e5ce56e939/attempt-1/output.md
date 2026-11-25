## REFORMULACION
Encargo ejecutable (`task.code`, no agregado): refactorizar el comando `specir mcp` para que `src/specir/mcp_extension.py` sea el único punto de `src/specir` que importe `sldb.mcp`. Resultado esperado: `specir mcp` conserva comportamiento y pasan `tests/test_imports.py` y `tests/test_cli_mcp.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: tocar `src/specir/cli.py`, `src/specir/mcp_extension.py` y, opcionalmente, `tests/test_cli_mcp.py`; no modificar `tests/test_imports.py`. Rituales aplicables: ejecución, testing y closeout.

## AMBIGUEDADES
1. “level=READ si None” y “serve(store, level=None, actor=None)”: obliga a inventar dónde se resuelve `None` a `READ`, con qué constante y si `actor` también tiene fallback.
2. “importa sldb.mcp.server y sldb.mcp.mutability” frente a “Mover la llamada a sldb.mcp.server.serve(...)”: obliga a inventar qué hacer con `sldb.mcp.mutability` (eliminarlo, moverlo o conservarlo en la extensión).
3. “si hace falta, tests/test_cli_mcp.py”: obliga a inventar el criterio de “hace falta” y qué cambios de test son aceptables.
4. “cli.py:mcp importa specir.mcp_extension.serve (lazy, dentro del comando) y le pasa los argumentos”: obliga a inventar el mapeo exacto entre flags/estado del CLI y `store`, `level`, `actor`.
5. “no usar los nombres MCPServer, FastMCP, build_server ni .run("stdio") en src/specir”: obliga a inventar si se audita todo `src/specir` o solo el código nuevo/tocado.

## DRY-RUN
Lecturas futuras: TaskDoc, rituales enrutados, `src/specir/cli.py`, `src/specir/mcp_extension.py`, `tests/test_imports.py`, `tests/test_cli_mcp.py`; pills/átomos están vacíos. Cambios previstos: añadir `serve(store, level=None, actor=None)` en `mcp_extension.py`, centralizar allí import y llamada a `sldb.mcp.server.serve`, importar esa función de forma lazy en `cli.py:mcp`, ajustar help de `--level` y, si procede, tests. Dependencias: API real de `sldb.mcp.server.serve`, semántica de `extensions`, parsing del CLI y expectativas de tests. Validación futura: primero prueba focalizada; después el comando indicado; además revisar imports/nombres prohibidos y que el comportamiento del comando no cambie. Sin ejecutar nada.

## FUTURO
Un nodo ejecutor implementará el parche y correrá la validación; el ritual de closeout actualizará board/átomos y preparará el commit. Un humano debe resolver las ambigüedades 1–5 y aprobar cualquier cambio de tests.
