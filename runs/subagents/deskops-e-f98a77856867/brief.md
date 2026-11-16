# Brief del ejecutor deskops-e-f98a77856867 (fixture mount_copy, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-f98a77856867` (rol executor, intento 1, contract_sha256 `43f09b39721ee252d24d047ada67c4c5092d7696f6f3d65db2e1c0e7a8024f64`). Implementas solo el alcance, dejas la evidencia y te detienes. **No commiteas, no cierras la tarea, no avanzas el desk y no lanzas agentes.**

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí, porque tu pane arrancó en el directorio padre. Usa `TMPDIR=/dev/shm` y `.venv/bin/python`.
- Run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-f98a77856867/`.
- Tarea: `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`. Lee `desk/tasks/<id>.md` completo, junto con sus disposiciones en `desk/reviews/<id>/`. El contrato es ese archivo.
- Solo tocas `tests/conftest.py`. En el checkout hay 5 archivos sin commitear de otra tarea (IR13e): `tests/visual/test_notations_parity.py`, `tests/visual/fixtures/spec2viz-notations/`, `src/specir/visual/notation_style.py` y `docs/spec2viz/{matriz-de-cobertura,acta-de-retiro}.md`. No los toques. Tampoco toques `desk/`, `.sldb/` ni `runs/` (salvo tu run dir).
- Prohibido: `git add`, `git commit`, `git stash`, `--autostash`, `pkill` y `pgrep`. Sin mocks.
- Valida:
  1. `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py` debe dar 5 passed y rc 0.
  2. La **suite completa, una sola vez, bajo el lock**: `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`. Antes mira `free -g` y espera si hay menos de 8 GB disponibles. La cola del lock puede tardar: no le pongas un tope corto.
  3. `deskops graph missing --root .`.
- Deja en tu run dir:
  - `validation.log`, con los comandos, su salida y su rc;
  - `result-summary.md`;
  - `git status --short > git-status.txt` y `git diff tests/conftest.py > diff.patch`.
- Al terminar, responde en una línea: `EJECUTOR TERMINADO: <ruta de result-summary.md>`, o `EJECUTOR BLOQUEADO: <motivo>`.
