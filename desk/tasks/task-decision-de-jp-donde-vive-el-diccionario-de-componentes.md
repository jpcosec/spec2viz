---
sldb:
  by: agent
  at: '2026-11-25T05:28:04Z'
  authority: generated
  via: create_document
id: task-decision-de-jp-donde-vive-el-diccionario-de-componentes
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
---

# Decision de JP: donde vive el diccionario de componentes

## Rationale

_Explain why this task exists or the business driver behind it._

D5 del plan graph_ui (desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md seccion 8 y PROPUESTA-UI.md). La decide JP.

## Goal

_Describe the concrete result this task must produce._

Registrar la eleccion de JP y su razon.

## Scope

_State what is in scope and what is out of scope._

Solo la decision; las tareas hijas se crean despues de decidida.

## Implementation Path

_Outline the expected implementation route or affected surface._

Opciones: (a) en el store del proyecto que se prueba (graph_ui), con specIR instalado ahi (recomendada: las anclas quedan junto al codigo); (b) en un store aparte de IR. Desbloquea T13.

## Validation

_List the checks required before this task can close._

- deskops show task <esta tarea> muestra la decision de JP

## Done When

_Name the observable condition that makes the task complete._

JP dispone el recibo de owner con la opcion elegida.
