# IR13j — resultado del ejecutor deskops-e-ab9406eaab99 (intento 1)

Tarea: `task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s`
(contract_sha256 `b577d7891a61c2f4c20a263acd532cce07d426ba22007c9b61d1b7c463ac0e63`). Sin commit, sin `git add`.

## Mensaje real de sldb

Comprobado con `probe-mensaje-sldb.py` (copia en este run dir; salida en `validation.log`), sobre la
notación `MINIMAL` de la prueba con `diagram_type: mindmap`:

- `load_notation(<ruta>)` (vía `specir.visual.notation_style`) → `sldb.notations.errors.validation_error.ValidationError`
- `NotationSpec.model_validate(...)` → `pydantic_core.ValidationError`

Ambos con el texto: `diagram_type 'mindmap' is not a valid diagram type`. Coincide con lo que sldb fija
como contrato en la nota de inbox 20261116-232335.

## Cambio en la prueba

`tests/visual/test_notations_parity.py`: el caso changes1 de `test_invalid_notations_are_rejected`
(línea 229) deja de ser `pytest.param(..., marks=xfail(strict=True))` y pasa a
`({"diagram_type": "mindmap"}, "diagram_type 'mindmap' is not a valid diagram type")`, con el mismo
comparador que los demás casos (`pytest.raises(Exception)` + `message in str(excinfo.value)`). El docstring
de la prueba cita la decisión de sldb (nota 20261116-232335, respuesta a la 20261116-022332). Ninguna otra
expectativa cambia. Resultado: 89 passed, sin xfailed ni xpassed (antes 88 passed, 1 xfailed).

## Estado de SV-H01 y de las filas que dependen de ella

Buscado SV-H01 en la columna Falta de «Acreditación (IR13)»: solo la nombra SV-K21.

- **SV-H01: cumplida.** Su único faltante era el xfail estricto de changes1; ya pasa. Falta: `-`.
- **SV-K21: sigue abierta.** Ya no depende de SV-H01 (cumplida), pero le falta el comando de sldb que
  valide una notación (nota 20261115-192054). Falta reescrita a eso.
- SV-K18 (depende de SV-K21) no cambia: sigue abierta.

## Resumen y gates

- Matriz: resumen 97 cumplidas, 8 abiertas (tras IR13j) — recuento de la tabla: 97 `cumplida`, 8 `abierta`
  (SV-A17, K09, K16, K18, K21, K23, K26, K29). Párrafo IR13j nuevo tras el de IR13g. G1: 8 filas abiertas,
  IR13j acreditó SV-H01. G2: la mención del xfail de SV-H01 se actualizó (ya no es xfail), porque si no
  la matriz se contradecía; es la única línea tocada fuera de resumen/G1/filas.
- Acta: encabezado (8 filas, corrida de IR13j), bloque de corrida nuevo de IR13j en el formato del de IR13h,
  fila G1, fila G2 (89 passed y quitado el xfail de SV-H01), punto 3 de «Lo que falta».
- Párrafos históricos (IR13e, IR13g) y las citas «(IR13e: 88 passed, 1 xfailed)» de otras filas no se tocan:
  registran esas corridas.

## Corrida del comprobador

`timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb`
(2026-11-17 01:23 -03:00; repetida a las 01:28 en `validation.log`): rc 1; 63 dependencias (sldb 1, IR 43,
`spec2viz/.sldb` 19; graph_ui, deskops y pron 0); 8 filas no acreditadas: SV-A17, K09, K16, K18, K21, K23,
K26, K29 — las mismas 8 abiertas de la matriz. Las 63 líneas son idénticas a la salida que ya estaba en el
acta (diff vacío). Sobre IR `c1a1a46` (sin commitear lo de IR13j), sldb `472f1c80`, graph_ui `440a5683`
(44 rutas sin commitear), deskops `cfda261b`, pron `39ea972`, spec2viz `91ba1d0`. Salida completa en
`retirement-check.out`. La corrida previa a editar la matriz daba 9 filas (con SV-H01).

## Validación (`validation.log`)

- `pytest -q -rxX tests/visual/test_notations_parity.py`: 89 passed, rc 0.
- `specir retirement check`: rc 1 (esperado: el retiro no se declara), 8 filas = 8 abiertas de la matriz.
- `pytest -q tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py`: 11 passed,
  1 xfailed, rc 0 (el xfail es `test_the_real_universe_has_no_dependency_and_every_row_is_accredited`,
  esperado mientras el retiro no se declare; fuera del alcance).
- `git diff --stat`: fuera de `desk/`, `.sldb/` y `runs/`, solo los 3 archivos de la tarea.
- `deskops graph missing --root .`: rc 0.

## Pendiente

- Cierre de la tarea (tester, commit, closeout): no es del ejecutor.
- SV-K21 / SV-K18 siguen abiertas por el comando de sldb que valide una notación; G1–G5 siguen abiertos.
