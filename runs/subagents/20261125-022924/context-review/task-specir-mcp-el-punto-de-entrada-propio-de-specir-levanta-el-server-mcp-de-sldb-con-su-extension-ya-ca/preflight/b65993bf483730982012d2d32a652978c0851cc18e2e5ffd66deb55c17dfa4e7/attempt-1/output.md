## REFORMULACION

Nodo `task.code` ejecutable (no agregado). Propósito: que specIR tenga punto de entrada MCP propio sin duplicar el server de sldb, reutilizando el mecanismo de extensión. Resultado observable: `specir mcp --store <ruta> [--level N] [--actor A]` arranca `sldb.mcp.server.serve` con `specir.mcp_extension:register`, `--help` lo explica y quedan disponibles las tools `specir_types`, `specir_nodes`, `specir_rules`, `specir_impact`. Repo: `/mnt/ssd/proyectos/SLDB_1/IR` (src/ y tests/ dentro). Límites: solo `src/specir/cli.py`, un test nuevo `tests/test_cli_mcp.py` y una línea en `skills/use-specir/SKILL.md`; fuera: sldb y `mcp_extension.py`.

## AMBIGUEDADES

1. «--level (int, default sldb.mcp.mutability.READ)»: el default es un símbolo de mutabilidad, no un entero, y el test (c) exige que llegue «level READ». Habría que inventar si la opción click es `int` con conversión al enum, o si acepta el enum/str, y si `serve` recibe entero o enum.
2. «siguiendo como tests/test_mcp_extension.py arma un store»: el input no transcribe ese montaje; obliga a inferir fixture, ruta de store y limpieza. Si ese fichero no contuviera el patrón, habría que inventarlo.
3. «su test» (Scope) frente a «Test NUEVO tests/test_cli_mcp.py»: podría leerse como test ya existente del CLI; se resuelve por Implementation Path, pero la formulación es ambigua.
4. «llama sldb.mcp.server.serve(store, level=level, actor=actor, extensions=(...))»: no se declara la firma real; si difiere en nombres/orden, el ejecutor debe decidir adaptar la llamada o fallar.

## DRY-RUN

Lecturas: `src/specir/cli.py`, `tests/test_mcp_extension.py`, `skills/use-specir/SKILL.md`, y firmas de `sldb.mcp.server.serve`, `build_server`, `load_extension`, `mutability`. Cambios previstos: comando click `mcp` montado en `main` con tres opciones y docstring de una línea; `tests/test_cli_mcp.py` con casos (a) cuatro tools, (b) `--help` sale 0 y nombra `--store`, (c) monkeypatch de `serve` capturando `extensions` y `level`; una línea en SKILL.md. Dependencias: API pública de sldb y `specir.mcp_extension:register`. Validación futura: el pytest indicado (`tests/test_cli_mcp.py` + `tests/test_mcp_extension.py`) con `PYTHONPATH=src` y `TMPDIR` dados; sin levantar stdio.

## FUTURO

Decide un humano: confirmar firma real de `serve` y política de `--level`/`--actor`. Otro nodo produce la implementación y ejecuta la validación; este preflight no ejecuta nada.
