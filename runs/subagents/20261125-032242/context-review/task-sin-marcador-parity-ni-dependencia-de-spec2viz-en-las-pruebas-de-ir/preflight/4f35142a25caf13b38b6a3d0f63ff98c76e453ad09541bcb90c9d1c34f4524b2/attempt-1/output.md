## REFORMULACION

**Propósito:** actualizar la descripción del marcador `parity` en `pyproject.toml` para que refleje el estado real: las pruebas de paridad comparan contra goldens congelados de spec2viz (revisión 2de1056) y no requieren spec2viz instalado.

**Resultado:** una sola entrada modificada en `[tool.pytest.ini_options] markers`, con el texto indicado, y `pytest -m parity -rs` sobre `tests/visual` sin skips.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`.

**Límites:** no quitar el marcador, no tocar tests, no alterar pruebas que mencionan spec2viz como dato (`test_packaging.py`, `test_retirement_gate.py`).

## AMBIGUEDADES

1. **Sintaxis TOML exacta.** Cita: *"Reemplazar en pyproject.toml el texto del marcador por: 'parity: compares specIR with the frozen spec2viz outputs (revision 2de1056) in tests/visual/goldens/; spec2viz is not needed'"*. No muestra la línea actual ni si `markers` es lista multilínea, ni el tipo de comillas. Obliga a inventar el formato exacto de sustitución.

2. **Criterio de "0 skipped".** Cita: *"confirmar 0 skipped"* y *"pasa sin skipped"*. ¿Cero skips absolutos en `tests/visual` o cero skips atribuibles a falta de spec2viz? Si existieran skips por otras causas, el criterio no lo distingue; obliga a decidir el criterio de aceptación.

3. **Entorno de ejecución en Implementation Path.** Cita: *"Correr pytest -m parity -rs sobre tests/visual"*. No precisa si se usa el comando exacto de Validation (`PYTHONPATH=src`, `TMPDIR`, `.venv/bin/python`) o el `pytest` del entorno activo. Obliga a asumir el entorno.

4. **Alcance real de los goldens.** Cita: *"tests/visual/goldens/spec2viz-2de1056*.json"*. El patrón no confirma qué archivos existen ni que cubran todos los tests `parity`; obliga a asumir cobertura.

## DRY-RUN

**Lecturas:** `pyproject.toml` (sección `[tool.pytest.ini_options]`, lista `markers`), `tests/visual/` y `tests/visual/goldens/`, y `git diff` para verificar alcance. **Cambios previstos:** sustituir únicamente la entrada del marcador `parity` por el texto indicado, respetando la sintaxis TOML existente. **Dependencias:** `.venv` del repo, `PYTHONPATH=src`, `TMPDIR=/mnt/ssd/tmp/sldb1`, goldens congelados. **Validaciones futuras:** ejecutar el comando de Validation, revisar la salida `-rs`, confirmar el criterio de skips acordado y comprobar con `git diff` que solo cambió `pyproject.toml`. Nada de esto se ejecuta aquí.

## FUTURO

Un humano o nodo revisor debe resolver las ambigüedades 1–2 antes de implementar. Después, un ejecutor aplica el cambio y corre la validación; un revisor o CI confirma que el diff se limita a `pyproject.toml` y que `parity` pasa; el cierre actualiza estado e historial.
