# Brief del tester deskops-t-8825fdd278af (fixture mount_copy, intento 1)

Eres el **tester independiente** de una tarea del desk IR, con la identidad `deskops-t-8825fdd278af` (rol tester, intento 1, contract_sha256 `43f09b39721ee252d24d047ada67c4c5092d7696f6f3d65db2e1c0e7a8024f64`). Tu rol es el de `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`: léelo primero.

Devuelves evidencia. **No implementas, no arreglas, no ruteas, no cierras y no commiteas.** No hagas `git add`, `commit`, `stash`, ni uses `pkill`/`pgrep`. Desconfía de lo que reporta el ejecutor.

## Dónde
- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR` (haz `cd` ahí; tu pane arrancó en el padre).
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-8825fdd278af/`.
- Usa `TMPDIR=/dev/shm` y `.venv/bin/python`.

## Qué pruebas
Tarea `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`: lee su archivo en `desk/tasks/` (Scope, Implementation Path, Validation, Done When) y las disposiciones en `desk/reviews/<id>/`.

El cambio está sin commitear en `tests/conftest.py` (`git diff tests/conftest.py`). OJO: en el checkout también hay cambios sin commitear de OTRA tarea (IR13e): `src/specir/visual/notation_style.py`, `docs/spec2viz/*`, `tests/visual/test_notations_parity.py`, `tests/visual/fixtures/spec2viz-notations/`. No son de esta tarea; no los evalúes, pero sí cuenta que esta tarea no los tocó (compara con `runs/subagents/deskops-e-31500ac1cfa1/diff.patch` si existe, o con lo que dice ese run dir).

El informe del ejecutor: `runs/subagents/deskops-e-f98a77856867/result-summary.md`. Léelo solo después de tu verificación.

## Verificaciones (todas con salida y rc en tu validation.log)
1. `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py` → 5 passed.
2. Mira `free -g`; si hay menos de 8 GB disponibles, espera y vuelve a mirar. Luego la suite completa UNA vez bajo el lock:
   `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/` → rc 0.
3. `deskops graph missing --root .` → rc 0.
4. Revisión del diff contra el contrato: solo copia `runs/subagents/*/run.md` (nada más de runs/), a la misma ruta relativa; constante declarada; docstring actualizado; no cambia `original_digest`/`copy_digest`/`FEDERATED`; sin mocks.
5. Que el cambio de esta tarea fuera de desk/.sldb/runs sea solo `tests/conftest.py`.

## Qué dejas
- `validation.log` con cada comando, salida y rc.
- `result-summary.md`: PASS/FAIL por verificación con evidencia, discrepancias con el ejecutor, veredicto final.

Al terminar responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
