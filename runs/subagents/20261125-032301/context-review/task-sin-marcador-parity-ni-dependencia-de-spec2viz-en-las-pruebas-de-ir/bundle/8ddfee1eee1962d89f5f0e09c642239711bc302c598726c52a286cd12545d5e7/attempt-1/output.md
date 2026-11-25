**REFORMULACION**
El nodo es una tarea ejecutable (`task.code`), no un agregado. Propósito: actualizar en `pyproject.toml` la descripción del marcador `parity` para que refleje el estado real: comparación con goldens congelados de spec2viz, sin requerir spec2viz instalado. Resultado esperado: esa línea describe goldens en `tests/visual/goldens/` y la validación `pytest -m parity -rs tests/visual` pasa sin skips. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo la línea del marcador en `[tool.pytest.ini_options] markers`; no quitar el marcador, no tocar tests ni eliminar referencias a spec2viz en tests existentes.

**AMBIGUEDADES**
1. “Solo la linea del marcador en pyproject.toml ([tool.pytest.ini_options] markers)” frente a “Reemplazar en pyproject.toml el texto del marcador por: ‘parity: compares…’”. No consta la línea actual exacta, su formato, comillas, indentación ni si ocupa una o varias líneas. Inventaría la forma textual si no se lee `pyproject.toml`.
2. “confirmar 0 skipped” y “Ninguna prueba se salta por falta de spec2viz”. No queda claro si “0 skipped” exige cero skips totales en `tests/visual` o solo ausencia de skips del marcador `parity` por falta de spec2viz. Inventaría el criterio de aceptación si se interpreta literalmente.

**DRY-RUN**
Lecturas previstas: `pyproject.toml` para localizar la entrada `parity`; tests de `tests/visual` y nombres de goldens; opcionalmente `test_packaging.py` y `test_retirement_gate.py` para confirmar que no se modifican. Cambio previsto: sustituir únicamente el texto del marcador por la cadena indicada. Dependencias: intérprete `/mnt/ssd/proyectos/SLDB_1/.venv/bin/python`, pytest, `PYTHONPATH=src`, `TMPDIR=/mnt/ssd/tmp/sldb1`, goldens versionados; no spec2viz. Validación futura: ejecutar exactamente el comando de la sección Validation y revisar `-rs` para confirmar ausencia de skips relevantes. Sin ejecutar ahora.

**FUTURO**
Otro nodo o un humano decidirá el cierre/commit, actualizará el Board, reconciliará pills/átomos y resolverá si el criterio de “0 skipped” es global o limitado a `parity`.
