PASA

Task: task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp
Commit del ejecutor: e1149a515ff4fadb574045e872f1102da56d89ff

Archivos del commit:
- src/specir/cli.py
- src/specir/mcp_extension.py

Comprobaciones:
- `specir mcp` ya no importa `sldb.mcp`: delega en `specir.mcp_extension.serve`.
- `serve` en `mcp_extension.py` concentra la llamada a `sldb.mcp.server.serve`, conservando READ por defecto y la extensión `specir.mcp_extension:register`.
- El help de `--level` ya no nombra `sldb.mcp.mutability`.
- Ningún otro modulo de `src/specir` importa `sldb.mcp`.
- `tests/test_imports.py` (incluye test_only_the_extension_reaches_mcp y test_specir_has_no_mcp_server_of_its_own): 9 passed.
- `tests/test_cli_mcp.py`: 3 passed.
- `tests/test_mcp_extension.py`: 11 passed.

Nota de entorno: el interprete indicado en el encargo (`/mnt/ssd/proyectos/SLDB_1/.venv/bin/python`) no tiene pytest instalado; las pruebas se ejecutaron con `/mnt/ssd/proyectos/SLDB_1/IR/.venv/bin/python`, que sí lo tiene, con `PYTHONPATH=$PWD/src` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-954d54c95477`.
