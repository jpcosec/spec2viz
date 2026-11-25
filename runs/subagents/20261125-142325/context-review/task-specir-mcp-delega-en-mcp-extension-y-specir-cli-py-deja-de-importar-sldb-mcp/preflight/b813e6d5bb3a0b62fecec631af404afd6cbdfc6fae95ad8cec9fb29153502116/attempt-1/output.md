## REFORMULACION

Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/IR`, hacer que el comando `specir mcp` deje de importar `sldb.mcp.server` y `sldb.mcp.mutability` desde `src/specir/cli.py`; toda dependencia de `sldb.mcp` debe quedar encapsulada en `src/specir/mcp_extension.py`. Resultado esperado: `specir mcp` mantiene su comportamiento y pasan `tests/test_imports.py` y `tests/test_cli_mcp.py`, incluidas las reglas de que solo la extensión alcance `sldb.mcp` y de que `src/specir` no contenga `MCPServer`, `FastMCP`, `build_server` ni `.run("stdio")`. Límites: se tocan `cli.py`, `mcp_extension.py` y, opcionalmente, `tests/test_cli_mcp.py`; `tests/test_imports.py` queda fuera. No se redefine la regla de importación.

## AMBIGUEDADES

1. «`sldb.mcp.server.serve(store, level=READ si None, actor, extensions=('specir.mcp_extension:register',))`»: sintaxis incompleta y no ejecutable. Obliga a inventar el mapeo exacto de argumentos y de dónde sale `READ`.
2. «`serve(store, level=None, actor=None)`» frente a la firma anterior con `extensions`: no queda claro si la nueva función conserva `extensions` internamente o lo fija. Obliga a inventar la firma final.
3. «`level=READ si None`»: no se define si el valor por defecto se resuelve dentro de `mcp_extension` o en `cli.py`; tampoco qué símbolo es `READ`. Obliga a inventar import y lógica de defecto.
4. «si hace falta, tests/test_cli_mcp.py»: la validación ejecuta ese archivo siempre, pero el alcance lo hace opcional. Obliga a decidir si debe existir o crearse.
5. «El help de --level no debe nombrar el módulo de sldb como import (texto libre esta bien)»: no delimita qué texto exacto incumple. Obliga a inventar el criterio de revisión.
6. «no usar los nombres ... en src/specir»: no aclara si aplica solo al código nuevo o a todo el árbol, ni si incluye comentarios o strings. Obliga a inventar el alcance del grep.

## DRY-RUN

Lecturas: TaskDoc, `src/specir/cli.py` (líneas 66-67 y comando `mcp`), `src/specir/mcp_extension.py`, `tests/test_cli_mcp.py` y, solo lectura, `tests/test_imports.py`. Cambios previstos: añadir `serve(...)` en `mcp_extension.py` que importe `sldb.mcp.server` y, si procede, `mutability.READ`; sustituir en `cli.py:mcp` por import lazy de `specir.mcp_extension.serve`. Dependencias: API real de `sldb.mcp.server.serve`, constante `READ`, registro de extensión. Validaciones futuras: el comando pytest indicado y búsqueda textual de los nombres prohibidos en `src/specir`. Sin ejecución.

## FUTURO

El ejecutor produce el parche y evidencia de los tests; el nodo de validación ejecuta pytest y la comprobación textual; un humano decide los puntos 1-6 si el ejecutor no puede resolverlos con el código.
