FILE:desk/tasks/task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee.md
---
sldb:
  by: agent
  at: '2026-11-16T19:52:54Z'
  authority: generated
  via: save_document_payload
id: task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-131509-suggestion-ir13-graph-ui-ya-no-depende-de-spec2viz-79d63ee-closeout-c9b09f7.md
- task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
depends_on:
- task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/acta-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR13g Acreditar en la matriz y el acta que graph_ui ya no depende de spec2viz (79d63ee)

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui avisó con la nota de inbox 20261116-131509 que su master 79d63ee (closeout c9b09f7) ya no depende de spec2viz: producción, pruebas y empaquetado usan sldb.api.notations y ViewDoc de sldb. La matriz de cobertura y el acta de retiro todavía dejan abiertas por G4 de graph_ui la fila SV-H03 y su dependiente SV-K22, y registran a graph_ui como consumidor pendiente.

## Goal

_Describe the concrete result this task must produce._

La matriz y el acta reflejan que graph_ui ya no depende de spec2viz, y el acta tiene una corrida nueva del comprobador con las filas y dependencias que quedan.

## Scope

_State what is in scope and what is out of scope._

Dentro, solo en docs/spec2viz/matriz-de-cobertura.md y docs/spec2viz/acta-de-retiro.md. (1) Matriz: SV-H03 pasa a cumplida si su único faltante era G4 de graph_ui y sus pruebas en tests/visual/test_notations_parity.py pasan; SV-K22, que depende solo de SV-H03, pasa a cumplida; SV-K18 sigue abierta mientras dependa de SV-K21. Las filas del inventario de consumidores de graph_ui se marcan resueltas citando 79d63ee, y se actualizan el resumen de cumplidas y abiertas y los estados del gate. (2) Acta: la fila de graph_ui en Consumidores pasa a resuelto citando 79d63ee, c9b09f7 y la nota; G4 deja de nombrar a graph_ui como pendiente, y lo mismo el punto de Consumidores de Lo que falta; también se anota el pendiente sin efecto en specir que menciona la nota, el ci.yml de graph_ui. (3) Una corrida nueva de specir retirement check con las rutas de los consumidores, anotando filas abiertas, dependencias por repo y rc, igual que las corridas anteriores. Fuera: tocar código o pruebas; cambiar graph_ui; declarar el retiro; quitar spec2viz/.sldb del universo.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero la nota de inbox y las filas SV-H03, SV-K18 y SV-K22 de la matriz, su sección Acreditación (IR13) y el acta completa. Para verificar graph_ui: git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD sale con rc 0, y git -C ../UIs/graph_ui grep -nE 'from spec2viz|import spec2viz|spec2viz>=' HEAD no encuentra nada en código ni en empaquetado. Si alguna falla, la fila no se marca resuelta: se anota lo encontrado y se reporta. El comando del comprobador es el de las corridas anteriores del acta: timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb. Las filas no acreditadas que liste deben coincidir con las abiertas de la matriz. Comandos desde la raíz de IR, con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo los dos documentos.
- git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD sale con rc 0 y la salida de specir retirement check no tiene dependencias de graph_ui.
- Las filas no acreditadas de specir retirement check coinciden con las filas abiertas de la sección Acreditación (IR13) de la matriz.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

SV-H03 y SV-K22 quedan cumplidas en la matriz (o abiertas con un motivo verificado que no sea G4 de graph_ui), graph_ui figura como resuelto en el acta con 79d63ee, y el acta tiene la corrida nueva del comprobador con sus filas y dependencias.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

