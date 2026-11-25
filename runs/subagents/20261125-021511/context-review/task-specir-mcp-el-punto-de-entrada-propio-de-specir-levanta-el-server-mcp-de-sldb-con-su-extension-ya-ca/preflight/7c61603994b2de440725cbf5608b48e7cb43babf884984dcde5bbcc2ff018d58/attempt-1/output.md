## REFORMULACION
**Propósito:** dotar a specIR de un punto de entrada MCP propio sin duplicar el servidor de sldb. **Resultado:** `specir mcp --store <ruta> [--level N] [--actor A]` debe arrancar `sldb.mcp.server.serve` con `specir.mcp_extension:register`; `--help` debe explicarlo y las tools `specir_*` deben aparecer. **Repo:** el input usa rutas relativas (`src/specir/cli.py`, `tests/test_cli_mcp.py`) y `PYTHONPATH=src`; no declara la raíz. **Límites:** tocar únicamente `src/specir/cli.py`, su test y una línea de `skills/use-specir/SKILL.md`; fuera de alcance sldb y `mcp_extension.py`.

## AMBIGUEDADES
1. «src/specir/cli.py» y «PYTHONPATH=src»: no se fija si `src` cuelga de `/mnt/ssd/proyectos/SLDB_1` o de `.../SLDB_1/IR`; obligaría a inventar la raíz del repo.
2. «src/specir/cli.py (comando mcp), su test»: no aclara si el test se crea o se modifica; obligaría a inventar el estado previo.
3. «Test: build_server con la extension registra...»: no indica dónde se importa `build_server` ni su firma; obligaría a inventar API/import.
4. «'specir mcp --help' lo explica»: no especifica texto ni opciones mostradas; obligaría a inventar contenido.
5. «skills/use-specir/SKILL.md (una linea)»: no da la línea; obligaría a inventar su redacción exacta.
6. «[--level N] [--actor A]»: no fija valores por defecto ni tipos; obligaría a inventar su paso a `serve`.

## DRY-RUN
Hipótetico, sin ejecutar: un ejecutor leería `src/specir/cli.py`, `tests/test_cli_mcp.py`, `skills/use-specir/SKILL.md`, la firma de `sldb.mcp.server.serve` y, solo como referencia, `mcp_extension.py`. Añadiría el comando click `mcp` con `store`, `level`, `actor`, llamando a `serve(..., extensions=('specir.mcp_extension:register',))`; ajustaría/crearía el test para construir el server sin stdio y comprobar `specir_types`, `specir_nodes`, `specir_rules` y `specir_impact`; añadiría una línea a la skill. Dependencias: click, API MCP de sldb, pytest y la extensión. Validación prevista: el comando pytest indicado, sin ejecutarlo aquí.

## FUTURO
Un nodo ejecutor aplicará los cambios y correrá la validación; otro revisor comprobará el diff y el resultado. Un humano deberá resolver las ambigüedades y aprobar los textos de ayuda/skill antes del cierre.
