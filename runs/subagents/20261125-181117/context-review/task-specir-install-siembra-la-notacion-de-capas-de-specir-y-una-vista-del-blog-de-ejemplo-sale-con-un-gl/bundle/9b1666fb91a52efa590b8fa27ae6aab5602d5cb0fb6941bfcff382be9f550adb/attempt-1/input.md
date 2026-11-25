FILE:desk/tasks/task-specir-install-siembra-la-notacion-de-capas-de-specir-y-una-vista-del-blog-de-ejemplo-sale-con-un-gl.md
---
sldb:
  by: agent
  at: '2026-11-25T17:45:06Z'
  authority: generated
  via: create_document
id: task-specir-install-siembra-la-notacion-de-capas-de-specir-y-una-vista-del-blog-de-ejemplo-sale-con-un-gl
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# specir install siembra la notación de capas de specIR y una vista del blog de ejemplo sale con un glifo por nodo

## Rationale

_Explain why this task exists or the business driver behind it._

docs/decisiones/paridad-por-capacidades.md (JP, 2026-11-25): specIR declara y graph_ui dibuja. Los 11 tipos de dominio de specIR no tienen notación en el store, así que lo extraído del código no se puede ver. Hay un borrador validado en desk/drawer/plans/paridad-por-capacidades/specir-layers.yml (11 glifos, 11 links).

## Goal

_Describe the concrete result this task must produce._

Que instalar specIR en un store deje la notación de capas lista para que una ViewDoc la use.

## Scope

_State what is in scope and what is out of scope._

Dentro: los datos de notación de specIR y src/specir/install.py. Fuera: carriles por capa (dependen de una tarea de graph_ui), ORCA e IFML.

## Implementation Path

_Outline the expected implementation route or affected surface._

Partir del borrador del drawer. La notación es dato sembrado, igual que relation_types.yaml y rules.yaml.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_install.py tests/test_layers_notation.py

## Done When

_Name the observable condition that makes the task complete._

En un store nuevo con specir install y el blog de ejemplo extraído, sldb notations validate acepta la notación y resolver una vista con ella devuelve cada documento de dominio con su glifo y cada relación con su link, sin huecos.

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
Cold-bundle de la tarea task-specir-install-siembra-la-notacion-de-capas-de-specir-y-una-vista-del-blog-de-ejemplo-sale-con-un-gl: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- python -m pytest -q tests/test_install.py tests/test_layers_notation.py

