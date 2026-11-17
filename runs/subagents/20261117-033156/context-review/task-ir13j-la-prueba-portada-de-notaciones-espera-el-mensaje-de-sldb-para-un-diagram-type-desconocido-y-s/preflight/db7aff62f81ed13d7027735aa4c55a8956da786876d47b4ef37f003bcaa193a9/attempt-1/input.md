FILE:desk/tasks/task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s.md
---
sldb:
  by: agent
  at: '2026-11-17T03:09:17Z'
  authority: generated
  via: save_document_payload
id: task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-232335-suggestion-sldb-responde-ir04b-undo-changes-mensaje-de-notationspec-ir13e-y-regresi-n-de-b2.md
- task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb
depends_on: []
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
files:
- tests/visual/test_notations_parity.py
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/acta-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR13j La prueba portada de notaciones espera el mensaje de sldb para un diagram_type desconocido y SV-H01 queda acreditada

## Rationale

_Explain why this task exists or the business driver behind it._

En la nota de inbox 20261116-232335, sldb respondió a la nota 20261116-022332 de IR13e que conserva como contrato su mensaje, «diagram_type 'mindmap' is not a valid diagram type», y que el de spec2viz («not a spec2viz diagram type») no vuelve. Hoy tests/visual/test_notations_parity.py marca ese caso como xfail estricto (línea 230), y por ese xfail SV-H01 sigue abierta en la matriz de cobertura.

## Goal

_Describe the concrete result this task must produce._

El caso de mindmap de test_invalid_notations_are_rejected pasa esperando el mensaje de sldb, sin xfail, y SV-H01 queda acreditada si ese era su único faltante.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/visual/test_notations_parity.py, donde el caso changes1 de test_invalid_notations_are_rejected espera el mensaje de sldb y deja de ser xfail, con el docstring citando la decisión de sldb (nota 20261116-232335); docs/spec2viz/matriz-de-cobertura.md, donde SV-H01 pasa a cumplida si su único faltante era ese xfail y se actualizan el resumen y G1 (las filas que dependen de SV-H01, como SV-K21, se revisan pero siguen abiertas mientras les falte otra cosa); docs/spec2viz/acta-de-retiro.md, con G1, Lo que falta y una corrida nueva de specir retirement check con las 5 rutas, en el formato del bloque de IR13h. Fuera: cambiar otras expectativas de la prueba; tocar sldb; declarar el retiro.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer la nota de inbox, el caso en tests/visual/test_notations_parity.py y las filas SV-H01 y SV-K21 de la matriz con su sección Acreditación (IR13). Comprobar el mensaje real con sldb.api antes de fijarlo en la prueba: cargar con load_notation (vía specir.visual.notation_style) la notación del caso con diagram_type mindmap y leer el mensaje del error. El comprobador es timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb, y sus filas no acreditadas deben coincidir con las abiertas de la matriz. Comandos desde la raíz de IR, con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -rxX -p no:cacheprovider tests/visual/test_notations_parity.py sale con rc 0, sin xfailed ni xpassed.
- Las filas no acreditadas de specir retirement check coinciden con las abiertas de la matriz.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo los tres archivos de la tarea.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

El caso de mindmap pasa con el mensaje de sldb, la matriz y el acta reflejan el estado de SV-H01, y el acta tiene la corrida nueva.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir13j-la-prueba-portada-de-notaciones-espera-el-mensaje-de-sldb-para-un-diagram-type-desconocido-y-s: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

