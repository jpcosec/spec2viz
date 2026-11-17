# IR13j — resultado del tester deskops-t-d471ebbc6f77 (intento 1)

- Tarea: `task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s`
- Rol: tester. contract_sha256 `b577d7891a61c2f4c20a263acd532cce07d426ba22007c9b61d1b7c463ac0e63`.
- run_id `run-deskops-t-d471ebbc6f77`; session `scion://agent/deskops-t-d471ebbc6f77`; session_sha256: no disponible (sesión scion, sin archivo local).
- Sin `git add`, commit, stash ni cambios fuera de este run dir. Evidencia: `validation.log`, `suite.log`,
  `rerun.log`, `suite2.log`, `board.txt`, `task.txt`, `next.txt`, `graph.txt`, `git-status.txt`, `probe-mensaje-sldb.py`.

## Verificaciones

| # | Verificación | Resultado |
|---|---|---|
| 1 | Validation de la tarea, cada comando con su rc | **PASS** |
| 2 | Mensaje real de sldb y diff de la prueba | **PASS** |
| 3 | Matriz y acta (y G2) | **PASS** |
| 4 | Fuera de desk/, .sldb/ y runs/ solo los 3 archivos | **PASS** |
| 5 | Suite completa bajo el lock | **PASS** en la corrida 2 (ver nota: la corrida 1 falló por entorno) |

### 1. Validation (`validation.log`)
- `pytest -q -rxX tests/visual/test_notations_parity.py`: 89 passed, sin xfailed ni xpassed, rc 0.
- `specir retirement check` (5 rutas, timeout 300): rc 1 (esperado), 63 dependencias (sldb 1, IR 43,
  `spec2viz/.sldb` 19), 8 filas no acreditadas: SV-A17, K09, K16, K18, K21, K23, K26, K29 — exactamente las
  8 `abierta` de la matriz (recuento propio con awk: 97 cumplidas, 8 abiertas).
- `pytest -q tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py`: 11 passed,
  1 xfailed, rc 0. El xfail es el estricto de `test_retirement_gate.py:191` (retiro no declarado); archivo sin cambios respecto de HEAD.
- `git diff --stat` / `git status`: fuera de desk/.sldb/runs solo los 3 archivos.
- `deskops graph missing --root .`: «No missing graph references found.», rc 0.

### 2. Mensaje de sldb y prueba
- Sonda propia (`probe-mensaje-sldb.py`, sobre `load_notation("statechart")` con `diagram_type: mindmap`):
  `diagram_type 'mindmap' is not a valid diagram type`, de `sldb/src/sldb/notations/notation_spec.py:47`.
  Coincide con la nota de inbox 20261116-232335.
- Diff de `tests/visual/test_notations_parity.py` frente a HEAD: solo cambia el caso changes1 (de
  `pytest.param(..., xfail strict)` a la tupla con el texto de sldb) y el docstring de la prueba, que cita
  la nota. Mismo comparador que los demás (`pytest.raises(Exception)` + `message in str(...)`). No queda
  ningún `xfail` en el archivo. Las otras 14 expectativas son idénticas a HEAD.

### 3. Matriz y acta
- SV-H01: en HEAD su Falta era solo el xfail estricto → pasar a cumplida es correcto.
- Dependientes: en la columna Falta de HEAD solo SV-K21 nombra SV-H01. SV-K21 sigue abierta con
  Falta = «el comando de sldb que valide una notación» (correcto; antes «Depende de SV-H01; falta…»).
  SV-K18 (depende de K21) sigue abierta. Correcto.
- Resumen 97/8 = recuento propio. G1 (matriz y acta) dice 8 abiertas y que IR13j acreditó SV-H01. Correcto.
- Bloque nuevo del acta: mismo formato que el de IR13h (rc; dependencias; filas; fecha/hora; task id;
  comando y timeout; hashes; recuento por repo; motivo del cambio). Las 63 líneas de dependencias de mi
  corrida son idénticas a las listadas en el acta (diff vacío). sldb `472f1c80` y spec2viz/pron coinciden
  con los HEAD actuales; deskops `cfda261b` es ancestro del HEAD actual (`4dff74a9`) y graph_ui tiene ahora
  48 rutas sucias en lugar de 44: ambos se movieron después de la corrida del ejecutor, no es falsedad.
- **G2 (fuera de la lista literal del Scope):** la matriz y el acta decían «xfail estricto … SV-H01»; dejarlo
  habría contradicho el Goal (SV-H01 acreditada sin xfail). El texto nuevo (89 passed, sin xfail; mensaje
  de sldb como contrato, nota 20261116-232335) es cierto. Cabe en el Goal. Lo mismo vale para el
  encabezado «Retiro: no declarado» del acta (9 → 8 filas), también tocado y también cierto.
- Observación menor, no bloqueante: otras filas siguen citando «(IR13e: 88 passed, 1 xfailed)»; son citas
  fechadas de una corrida anterior (mismo criterio que usó IR13g), no afirmaciones del estado actual.

### 4. Archivos
`git status`: fuera de desk/, .sldb/ y runs/ solo `tests/visual/test_notations_parity.py`,
`docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`.

### 5. Suite completa (`SPECIR_MMDC=… TMPDIR=/dev/shm timeout 9000 flock /dev/shm/sldb1-tests.lock … -n 4 tests/`)
- Corrida 1 (`suite.log`, 10 GB disponibles al empezar): rc 1, 18 failed, 732 passed, 3 xfailed, 54 min.
  2 = fallo externo conocido. Los otros 16 (test_catalog, test_catalog_annotations, test_catalog_parity,
  test_cli, test_lint_mermaid, test_render_cases) fueron todos de mmdc/Chromium: «Failed to launch the
  browser process», timeout de 30 s del WS endpoint, rc 124/137. Durante la corrida el swap llegó a 15/15 GB
  por un proceso ajeno (`mepu.datos.consulta`, 7 GB RSS). Ninguno toca notaciones.
- Reejecución de esos 16, en serie y bajo el lock (`rerun.log`): 16 passed.
- Corrida 2 de la suite completa con el mismo comando (`suite2.log`, 15 GB disponibles): rc 1,
  **2 failed, 748 passed, 3 xfailed**. Los 2 son exactamente
  `test_sync_generation_parity.py::test_a_component_spec_from_specir_python_ast_validates` y
  `::test_python_ast_generation_of_specir_matches_spec2viz_up_to_the_declared_differences`, con
  `component-spec/syntax-error` sobre `visual/templates/vendor/bpmn-js/…` (regresión de B2 de sldb, con espejo en IR). Ajenos.

## Comparación con el informe del ejecutor
Todo lo que afirma `deskops-e-ab9406eaab99/result-summary.md` coincide con lo que verifiqué (89 passed,
8 filas = 8 abiertas, 63 dependencias idénticas, 11 passed + 1 xfailed, solo 3 archivos, graph missing rc 0,
SV-K21/K18 abiertas, alcance de G2). Sin discrepancias. El ejecutor no corrió la suite completa; la corrí yo.

## Veredicto
**PASS.** No hay defectos en el cambio. Lo único fuera del guion es que la corrida 1 de la suite falló por
memoria (16 fallos de navegador); se reejecutó, y la corrida 2 deja solo el fallo externo conocido. Antes del
closeout no hace falta nada más.
