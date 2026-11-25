REFORMULACION
El encargo es una tarea de código (`task.code`), no un agregado ni un paquete no ejecutable. Propósito: dar a specIR un punto de entrada MCP propio sin duplicar el server de sldb. Resultado: `specir mcp --store <ruta> [--level N] [--actor A]` arranca `sldb.mcp.server.serve` con la extensión `specir.mcp_extension:register`; `--help` lo explica y aparecen las tools `specir_*`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: tocar `src/specir/cli.py`, crear `tests/test_cli_mcp.py` y añadir una línea en `skills/use-specir/SKILL.md`; fuera: sldb y `mcp_extension.py`.

AMBIGUEDADES
1. “--level (int, default sldb.mcp.mutability.READ)”: no consta que `READ` sea un `int`; si no lo es, habría que inventar conversión o tipo Click.
2. “siguiendo como tests/test_mcp_extension.py arma un store”: el helper exacto no está en el bundle; si no es reutilizable, habría que inventar la construcción del store.
3. “un comando click 'mcp' montado en main” y “su test”: no se explicita la forma actual de `main` ni si existe test previo; sin leer `cli.py`, habría que inventar decoradores/registro.

DRY-RUN
Lecturas: `src/specir/cli.py`, `tests/test_mcp_extension.py`, definiciones de `sldb.mcp.server.serve/build_server`, `sldb.mcp.extension.load_extension`, `sldb.mcp.mutability.READ`, y `skills/use-specir/SKILL.md`. Cambios: comando Click `mcp` con opciones indicadas y llamada a `serve(store, level=level, actor=actor, extensions=('specir.mcp_extension:register',))`; test nuevo con (a) cuatro tools, (b) help, (c) monkeypatch de `serve`; línea documental. Dependencias: Click, sldb instalado, fixture del test existente, firma real de `serve`. Validación futura: el comando pytest indicado, sin levantar stdio. Pills, átomos y archivos del frontmatter están vacíos.

FUTURO
Otro nodo ejecutor implementará y correrá la validación; closeout actualizará board y preparará commit. Si la firma de `serve` o el helper difieren, se resolverá leyendo el repo, no inventando. Un humano decide cualquier ajuste de alcance si la validación falla.
