# Brief del tester deskops-t-c8a1e07fdf14-a2 (IR13e, intento 2: tras el ciclo de corrección 1)

Eres el **tester independiente** de una tarea del desk IR, con la identidad `deskops-t-c8a1e07fdf14-a2` (rol tester, intento 2, contract_sha256 `e14875086fa0666d1167e68b0083e15177e1d0395ce85f862640f6c6aafca8c8`). Tu rol es el de `/mnt/ssd/proyectos/SLDB_1/deskops/desk/roles/deskops-tester.md`: léelo primero.

Devuelves evidencia. **No implementas, no arreglas, no ruteas, no cierras y no commiteas.** Desconfía de lo que reporta el ejecutor: verifica todo por tu cuenta.

## Dónde

- Raíz: `/mnt/ssd/proyectos/SLDB_1/IR`. Haz `cd` ahí, porque tu pane arrancó en el directorio padre.
- Tu run dir: `/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-c8a1e07fdf14-a2/`.
- Usa siempre `TMPDIR=/dev/shm`, `.venv/bin/python` y `.venv/bin/specir`.

## Qué pruebas

La tarea es `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`. Lee su archivo en `desk/tasks/`, junto con su Scope, Implementation Path, Validation y Done When, y las disposiciones en `desk/reviews/task-ir13e-…/`.

El trabajo del ejecutor está **sin commitear** en el checkout. Revísalo con `git status --short` y `git diff`, más estos archivos nuevos:
- `tests/visual/test_notations_parity.py`
- `tests/visual/fixtures/spec2viz-notations/`

El informe del ejecutor está en `runs/subagents/deskops-e-3db2821b1604-a2/result-summary.md (el del intento 1 está en runs/subagents/deskops-e-31500ac1cfa1/)`. Léelo solo después de hacer tu propia verificación, para compararlo.

## Verificaciones (todas, con salida y rc en tu validation.log)

1. Corre uno por uno: `tests/visual/test_notations_parity.py -rxXs`, `tests/test_imports.py`, `tests/test_matriz_cobertura_spec2viz.py` y `tests/visual/test_retirement_gate.py`, todos con `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider`.
2. **Suite completa, una sola vez, bajo el lock:**
   `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/`
   Antes de correrla mira `free -g`. Si hay menos de 8 GB disponibles, espera y vuelve a mirar.
3. Los greps de la Validation de la tarea: ni `spec2viz` ni `sldb.(notations|models|store|core)` importados en el archivo nuevo.
4. `timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb`. Las filas no acreditadas que liste tienen que coincidir exactamente con las filas «abierta» de la sección «Acreditación (IR13)» de `docs/spec2viz/matriz-de-cobertura.md`.
5. `deskops graph missing --root .` debe salir con rc 0.
6. Comprobaciones de contrato, a mano:
   - Hay 42 pruebas portadas (precisión f: 42 + 9 = 51) y cada una cita en su docstring la prueba de spec2viz de origen. Compáralas con `../spec2viz/tests/{test_view_doc,test_notation,test_notation_view,test_view_contract_resolved,test_style_palette}.py`, excluyendo la parte CLI que nombra el scope; las dos nuevas (e1, e2) portan la parte no CLI de test_notation_validate_gives_typed_errors y test_palette_validation_is_typed.
   - Hay 9 comparaciones «valida igual».
   - Las expectativas de cada prueba portada son las mismas de spec2viz: nada se suavizó. Los xfail son estrictos y su razón es real.
   - Las fixtures copiadas son idénticas a las de `git -C ../spec2viz show b624b75:<ruta>`.
   - `notation_style.py` solo agrega reexportaciones.
   - Las 18 filas de la matriz (las 16 del scope más SV-G08 y SV-I02) están cumplidas solo si todas sus pruebas pasan sin xfail, y si no, abiertas con su motivo.
   - No se tocó ningún archivo fuera de los 5 del scope (los cambios en `desk/`, `.sldb/` y `runs/` son del coordinador).

## Qué dejas

- `validation.log`, con cada comando, su salida y su rc.
- `result-summary.md`: veredicto **PASS** o **FAIL** por cada verificación, con la evidencia; las discrepancias con el informe del ejecutor; y un veredicto final. FAIL si algo no se cumple.

Al terminar, responde en una línea: `TESTER TERMINADO: PASS|FAIL <ruta de result-summary.md>`.

## Contexto del intento 2

El tester del intento 1 dio FAIL por dos motivos. El primero fue un XPASS del label_key de test_catalog.py, que ya se resolvió en 4dc8946. El segundo fue que SV-H04 y SV-H06 se acreditaban sin portar la validación tipada no CLI. El contrato añadió las precisiones (e)–(h): léelas. Verifica en particular:
- e1 y e2 existen, tienen los 7 y 6 casos de origen (`git -C ../spec2viz show b624b75:tests/test_style_palette.py`) y conservan las mismas expectativas;
- la correspondencia de la precisión (g) en la matriz;
- que la acreditación de SV-H06 se sostiene con el contrato;
- `pytest -rxX tests/visual/test_catalog.py` (con SPECIR_MMDC) da 0 xfail y 0 xpass de label_key;
- que el acta refleja la salida actual del comprobador.

`tests/conftest.py` ya está commiteado (9c30a40) y no forma parte de esta tarea. Si el lock de la suite está tomado por otra sesión, espera con un timeout amplio (9000 s sobre espera + ejecución); un rc 124 del timeout no es un fallo de las pruebas.
