---
sldb:
  by: agent
  at: '2026-11-16T15:46:03Z'
  authority: generated
  via: save_document_payload
id: task-espejo-deskops-deskops-sldb-deja-de-enlazar-el-store-de-spec2viz-g5-opción-b
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- ../deskops/desk/inbox/20261116-122447-suggestion-deskops-sldb-enlaza-spec2viz-las-pruebas-mcp-de-ir-leen-el-store-real-de-spec2viz-de-forma-transitiva-g5.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Espejo deskops: deskops/.sldb deja de enlazar el store de spec2viz (G5, opción b)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de un trabajo del desk de deskops, para que depends_on lo exprese con un id local que deskops resuelve. El trabajo vive en deskops. JP decidió el 2026-11-16 la opción b: no se ajusta el Done When de la tarea de IR que deja de federar el store real de spec2viz en las pruebas MCP, y deskops quita de su store el enlace al store de spec2viz.

## Goal

_Describe the concrete result this task must produce._

Que el store de deskops deje de enlazar el store de spec2viz, para que las pruebas MCP de IR, que federan el store real de deskops, ya no lean el store de spec2viz de forma transitiva.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado del trabajo de deskops pedido en la nota de su inbox 20261116-122447 (repo registrado como deskops). Cuando deskops cree su tarea, su id se agrega a las referencias de este espejo. Fuera: cualquier trabajo en IR; el cambio se hace y se cierra en el desk de deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. El espejo se cierra cuando deskops avisa que quitó el enlace, con un commit de deskops como evidencia externa, y cuando el store_index del store de deskops ya no nombra spec2viz.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

La tarea de deskops que quita el enlace al store de spec2viz está cerrada e integrada en la rama principal de deskops, y el store_index del store de deskops ya no enlaza spec2viz.
