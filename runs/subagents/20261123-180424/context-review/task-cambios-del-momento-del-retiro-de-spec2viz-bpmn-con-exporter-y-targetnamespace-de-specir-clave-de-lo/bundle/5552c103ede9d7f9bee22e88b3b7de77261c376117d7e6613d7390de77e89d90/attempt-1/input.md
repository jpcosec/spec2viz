FILE:desk/tasks/task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo.md
---
sldb:
  by: agent
  at: '2026-11-23T18:03:20Z'
  authority: generated
  via: save_document_payload
id: task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cambios del momento del retiro de spec2viz: BPMN con exporter y targetNamespace de specir, clave de localStorage del catalogo de specir con migracion y goldens nuevos

## Rationale

_Explain why this task exists or the business driver behind it._

Decision de JP del 2026-11-23 en task-jp-decide-declarar-el-retiro-de-spec2viz-sacar-spec2viz-sldb-del-universo-del-comprobador-y-archivar (recibo owner-1, punto 2): hacer ya los cambios del momento del retiro descritos en docs/spec2viz/acta-de-retiro.md, punto 8 (decision 3 del acta).

## Goal

_Describe the concrete result this task must produce._

El BPMN que emite specir lleva exporter='specir' y un targetNamespace de specir; la pagina del catalogo usa una clave de localStorage de specir y migra al cargar las anotaciones guardadas con spec2viz.catalog.annotations.v1 (sin perderlas y sin volver a escribir la clave vieja); los goldens afectados se regeneran con el comando del repo y quedan revisados en el diff.

## Scope

_State what is in scope and what is out of scope._

Emisor BPMN de specir, la pagina del catalogo (JS de localStorage) y sus goldens y tests en IR. Fuera: declarar el retiro en el acta y archivar el repo spec2viz (punto 3, lo hace el coordinador despues de attach_atom_edges en sldb); sacar spec2viz/.sldb del inventario y SV-A17 (punto 1, abierto).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ubicar con grep exporter=, targetNamespace y spec2viz.catalog.annotations.v1 en IR. 2) Cambiar el emisor BPMN y su test. 3) Clave nueva de localStorage con migracion desde la vieja y test (de JS o de la pagina generada). 4) Regenerar los goldens con el comando del repo y revisar el diff. 5) Marcar el punto 8 como hecho en el acta con fecha y commit.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los tests de BPMN, catalogo y goldens tocados

## Done When

_Name the observable condition that makes the task complete._

Los tests de BPMN y del catalogo pasan con los goldens nuevos; un test prueba la migracion de la clave vieja a la nueva; grep de spec2viz.catalog.annotations.v1 solo queda en la migracion; el acta registra el punto 8 hecho.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:instruccion
Cold-bundle de la tarea task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q de los tests de BPMN, catalogo y goldens tocados

