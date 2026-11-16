# Brief del ejecutor deskops-e-31500ac1cfa1 (IR13e, intento 1)

Eres el **ejecutor** de una sola tarea del desk IR, con la identidad `deskops-e-31500ac1cfa1` (rol executor, intento 1, contract_sha256 `5efb8cf1a77ffacdc67e55685465f67f4b64fabd59a2d004f7bc2043c7542b59`). Implementas solo el alcance de la tarea, dejas la evidencia y te detienes. **No cierras la tarea, no commiteas, no avanzas el desk y no lanzas a otros agentes.**

## Dónde

- Raíz de trabajo: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí antes de cualquier comando. Tu pane arrancó en el directorio padre; no trabajes allí.
- Run dir (tu evidencia): `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-e-31500ac1cfa1/`.
- Usa siempre `TMPDIR=/dev/shm` y el `.venv` de IR (`.venv/bin/python`, `.venv/bin/specir`).

## La tarea

Lee completa, con `deskops show task <id> --root .`, la tarea `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb` y también su archivo `desk/tasks/task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb.md`, con el Scope, el Implementation Path (y sus «Precisiones preflight-1», de la a a la d), la Validation y el Done When. El contrato es ese archivo; este brief no lo reemplaza.

Lee también:
- Los 4 pills que tiene ligados (`desk/contexts/pill-guardrail-*.md`).
- Las disposiciones aceptadas en `desk/reviews/task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb/` (preflight-2 y bundle-1). Esas disposiciones fijan:
  - el total: 40 pruebas portadas más 9 comparaciones, o sea 49;
  - el criterio de igualdad «valida igual»: el `model_dump()` de la notación o paleta cargada con sldb desde el YAML copiado debe ser igual al `model_dump()` de la builtin de sldb del mismo nombre;
  - el renderer de mermaid: `src/specir/visual/renderers/mermaid.py`;
  - ViewDoc: se intenta importarlo desde `sldb.api` y, si no existe, aplica la precisión (d).

## Reglas

- Archivos que puedes tocar, y ningún otro: `tests/visual/test_notations_parity.py` (nuevo), `tests/visual/fixtures/spec2viz-notations/` (nuevo), `src/specir/visual/notation_style.py`, `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`.
- `../spec2viz` y `../sldb` son de **solo lectura**. Verifica que `git -C ../spec2viz rev-parse --short HEAD` da `b624b75` y anótalo.
- Sin mocks ni datos fabricados. Si un caso no pasa contra sldb, no cambies la expectativa: márcalo con `pytest.mark.xfail(strict=True, reason=<la diferencia>)`, deja la fila abierta con esa diferencia y manda la nota a sldb con `deskops message send --to sldb --root . --kind suggestion --title ... "<cuerpo que cite la prueba>"`. Esa nota es la única escritura permitida fuera de los 5 archivos.
- No edites a mano nada bajo `desk/` ni `.sldb/`. No hagas `git add`, `git commit`, `git stash`, `git add -A` ni `--autostash`. No uses `pkill` ni `pgrep`.
- Tests: corre solo los puntuales, archivo por archivo y sin lock. **No corras la suite completa**: la corre el tester independiente bajo `/dev/shm/sldb1-tests.lock`.
- Si te bloquea algo que no está en el contrato, detente y anótalo en el informe. No improvises alcance.

## Validación que debes correr (desde IR)

```bash
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_notations_parity.py
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py
TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_retirement_gate.py
grep -nE '^(from|import) spec2viz' tests/visual/test_notations_parity.py ; grep -nE 'from sldb\.(notations|models|store|core)' tests/visual/test_notations_parity.py
timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb
deskops graph missing --root .
```

Si tocas `notation_style.py`, corre también, uno por uno, los tests de `tests/visual/` que lo importan (`grep -l notation_style tests -r`).

## Qué dejas en el run dir

- `validation.log`: cada comando de arriba, con su salida completa y su rc.
- `result-summary.md`:
  - los archivos tocados;
  - las 49 pruebas, con passed o xfailed y la razón de cada xfail;
  - cada una de las 16 filas, con su estado final y la prueba que la acredita o el motivo por el que sigue abierta;
  - las notas enviadas a sldb, con su id;
  - la salida resumida de `specir retirement check`: cuántas filas abiertas había antes (23) y cuántas quedan;
  - la revisión de spec2viz;
  - todo lo que quedó pendiente o bloqueado.
- `git -C /mnt/ssd/proyectos/SLDB_1/IR status --short > git-status.txt` y `git -C /mnt/ssd/proyectos/SLDB_1/IR diff --stat > diff-stat.txt`.

Cuando termines, responde en una línea: `EJECUTOR TERMINADO: <ruta de result-summary.md>`, o `EJECUTOR BLOQUEADO: <motivo>`.
