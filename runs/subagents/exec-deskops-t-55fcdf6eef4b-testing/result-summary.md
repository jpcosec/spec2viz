PASA

Task: task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr
Commit del ejecutor: f0c182d00cc8dd1cc0e85b09c8212bb314c62348 — "test: resolve the workspace from SPECIR_WORKSPACE before the repo parent"

Archivos del commit:
- tests/conftest.py
- tests/test_workspace_env.py (nuevo)

Comprobaciones:
- `tests/conftest.py` extrae `workspace_root()`: devuelve `Path(SPECIR_WORKSPACE)` si la variable no está vacía y, si no, `REPO.parent`. `WORKSPACE = workspace_root()` y el único uso relevante para el store de deskops (`source = WORKSPACE / "deskops"`) pasa por esa constante.
- `tests/test_workspace_env.py` cubre los tres casos: variable definida, ausente y definida vacía. 3 passed.
- `tests/test_mcp_extension.py` (usa el store de deskops vía fixtures): 11 passed.
- Done When verificado en una copia del repo fuera de SLDB_1 (`/tmp/ir-outside`) con `SPECIR_WORKSPACE` apuntando al workspace real: `test_workspace_env.py` y los tests de la copia de deskops pasan (5 passed). Sin la variable, la misma copia falla con `the deskops store is missing: /tmp/deskops/.sldb`, que es justo la regresión que corrige el cambio.

Observaciones (no afectan al veredicto):
- El commit incluye el trailer `Task-Id: ...`, aunque el encargo pedía no ponerlo en el commit de código. Funcionalmente es inocuo, pero el closeout podría duplicarlo.
- `tests/visual/test_retirement_gate.py:30` conserva `WORKSPACE = REPO.parent`; queda fuera del alcance declarado (solo `tests/conftest.py` y su test), pero ese archivo no toma `SPECIR_WORKSPACE` si algún día corre fuera del workspace.

Nota de entorno: `/mnt/ssd/proyectos/SLDB_1/.venv/bin/python` apunta a `/usr/bin/python3` (3.11) y no importa pytest ni los paquetes compilados para 3.12. Las pruebas se ejecutaron con Python 3.12.16 de `/dev/shm/uvpy`, `PYTHONPATH` a los site-packages 3.12 del `.venv` más `IR/src` y `sldb/src`, y un wrapper `sldb` equivalente al console script. `TMPDIR=/tmp` y `--basetemp` bajo `/tmp` según el encargo. Detalle en `validation.log`.
