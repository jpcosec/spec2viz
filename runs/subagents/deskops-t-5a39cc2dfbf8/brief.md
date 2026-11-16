# Brief del tester deskops-t-5a39cc2dfbf8 (IR13e, intento 1)

Eres el **tester independiente** de una tarea del desk IR, con la identidad `deskops-t-5a39cc2dfbf8` (rol tester, intento 1, contract_sha256 `5efb8cf1a77ffacdc67e55685465f67f4b64fabd59a2d004f7bc2043c7542b59`). Tu rol es el de `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`: léelo primero.

Devuelves evidencia. **No implementas, no arreglas, no ruteas, no cierras y no commiteas.** Desconfía de lo que reporta el ejecutor: verifica todo por tu cuenta.

## Dónde

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí, porque tu pane arrancó en el directorio padre.
- Tu run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-5a39cc2dfbf8/`.
- Usa siempre `TMPDIR=/dev/shm`, `.venv/bin/python` y `.venv/bin/specir`.

## Qué pruebas

La tarea es `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`. Lee su archivo en `desk/tasks/`, junto con su Scope, Implementation Path, Validation y Done When, y las disposiciones en `desk/reviews/task-ir13e-…/`.

El trabajo del ejecutor está **sin commitear** en el checkout. Revísalo con `git status --short` y `git diff`, más estos archivos nuevos:
- `tests/visual/test_notations_parity.py`
- `tests/visual/fixtures/spec2viz-notations/`

El informe del ejecutor está en `runs/subagents/deskops-e-31500ac1cfa1/result-summary.md`. Léelo solo después de hacer tu propia verificación, para compararlo.

## Verificaciones (todas, con salida y rc en tu validation.log)

1. Corre uno por uno: `tests/visual/test_notations_parity.py -rxXs`, `tests/test_imports.py`, `tests/test_matriz_cobertura_spec2viz.py` y `tests/visual/test_retirement_gate.py`, todos con `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider`.
2. **Suite completa, una sola vez, bajo el lock:**
   `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`
   Antes de correrla mira `free -g`. Si hay menos de 8 GB disponibles, espera y vuelve a mirar.
3. Los greps de la Validation de la tarea: ni `spec2viz` ni `sldb.(notations|models|store|core)` importados en el archivo nuevo.
4. `timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb`. Las filas no acreditadas que liste tienen que coincidir exactamente con las filas «abierta» de la sección «Acreditación (IR13)» de `docs/spec2viz/matriz-de-cobertura.md`.
5. `deskops graph missing --root .` debe salir con rc 0.
6. Comprobaciones de contrato, a mano:
   - Hay 40 pruebas portadas y cada una cita en su docstring la prueba de spec2viz de origen. Compáralas con `../spec2viz/tests/{test_view_doc,test_notation,test_notation_view,test_view_contract_resolved,test_style_palette}.py`, excluyendo las 6 de CLI que nombra el scope.
   - Hay 9 comparaciones «valida igual».
   - Las expectativas de cada prueba portada son las mismas de spec2viz: nada se suavizó. Los xfail son estrictos y su razón es real.
   - Las fixtures copiadas son idénticas a las de `git -C ../spec2viz show b624b75:<ruta>`.
   - `notation_style.py` solo agrega reexportaciones.
   - Las 16 filas de la matriz están cumplidas solo si todas sus pruebas pasan sin xfail, y si no, abiertas con su motivo.
   - No se tocó ningún archivo fuera de los 5 del scope (los cambios en `desk/`, `.sldb/` y `runs/` son del coordinador).

## Qué dejas

- `validation.log`, con cada comando, su salida y su rc.
- `result-summary.md`: veredicto **PASS** o **FAIL** por cada verificación, con la evidencia; las discrepancias con el informe del ejecutor; y un veredicto final. FAIL si algo no se cumple.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.
