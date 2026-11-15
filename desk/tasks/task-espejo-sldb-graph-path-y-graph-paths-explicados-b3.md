---
sldb:
  by: agent
  at: '2026-11-15T16:51:33Z'
  authority: generated
  via: create_document
id: task-espejo-sldb-graph-path-y-graph-paths-explicados-b3
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Espejo sldb: graph_path y graph_paths explicados (B3)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de una tarea del desk de sldb, para que depends_on la exprese con un id local que deskops resuelve; el trabajo vive en sldb.

## Goal

_Describe the concrete result this task must produce._

Disponer en sldb de caminos explicados en el recorrido del grafo, con la procedencia de cada tramo, para el impacto de specIR.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado de la tarea de sldb task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3 (desk de sldb, repo registrado como sldb). Fuera: cualquier trabajo en IR; el cambio se pide y se cierra en el desk de sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando la tarea de sldb task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3 está cerrada, con un commit de sldb como evidencia externa.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

La tarea de sldb task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3 está cerrada y integrada en la rama principal de sldb.
