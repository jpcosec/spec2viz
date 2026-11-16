# Brief del ejecutor deskops-e-f5f68a7aa648 (xfail label_key, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-f5f68a7aa648` (rol executor, intento 1, contract_sha256 `3514030a81810539d75c002be92c7ad41dce1fcaa58bc434e7fac57bdeec37d0`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

## Dónde
- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de cualquier comando, porque tu pane arrancó en el padre.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-f5f68a7aa648/`.
- Usa `TMPDIR=/dev/shm` y el `.venv` de IR.

## La tarea
`task-quitar-el-xfail-obsoleto-de-label-key-en-test-catalog-tras-el-arreglo-de-sldb-06dbcf02`. Léela completa en `desk/tasks/<id>.md`, junto con su pill y las disposiciones aceptadas en `desk/reviews/<id>/` (preflight-2 y bundle-1). El contrato es el TaskDoc.

## Reglas
- Solo puedes tocar `tests/visual/test_catalog.py`, y solo para borrar la línea del decorador `@pytest.mark.xfail(strict=True, ...)` de `test_label_key_of_sldb_splits_underscores_like_norm_key` (hoy es la línea 521). El diff esperado es una sola línea borrada.
- En el árbol hay cambios sin commitear de otras tareas que **no tocas**:
  - `tests/conftest.py`: es la tarea del fixture y es precondición. Antes de nada comprueba que `git diff --stat tests/conftest.py` lo lista y que `git diff tests/conftest.py | grep RUN_DOCS` encuentra algo.
  - Los 5 archivos de IR13e: `tests/visual/test_notations_parity.py`, `tests/visual/fixtures/spec2viz-notations/`, `src/specir/visual/notation_style.py`, `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`.
- `../sldb` es solo lectura.
- No edites `desk/` ni `.sldb/`. No hagas `git add`, `git commit`, `git stash` ni `--autostash`. No uses `pkill` ni `pgrep`.
- **No corras la suite completa**: la corre el tester bajo el lock. Corre solo las pruebas puntuales.
- Si la prueba falla sin el xfail, detente y repórtalo, sin cambiar la aserción.

## Validación (desde IR; todo en validation.log con su rc)
```bash
git -C ../sldb merge-base --is-ancestor 06dbcf02 HEAD; echo rc=$?
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider "tests/visual/test_catalog.py::test_label_key_of_sldb_splits_underscores_like_norm_key"   # antes: XPASS(strict) -> failed
# editar
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider "tests/visual/test_catalog.py::test_label_key_of_sldb_splits_underscores_like_norm_key"   # después: passed
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider -rxX tests/visual/test_catalog.py
git diff tests/visual/test_catalog.py
deskops graph missing --root .
```

## Qué dejas en el run dir
- `validation.log`.
- `result-summary.md`, con el cambio, cada resultado y lo que haya quedado pendiente.
- `diff.patch`: la salida de `git diff tests/visual/test_catalog.py`.
- `git-status.txt`: la salida de `git status --short`.

Al terminar responde en una línea: `EJECUTOR TERMINADO: <ruta de result-summary.md>` o `EJECUTOR BLOQUEADO: <motivo>`.
