---
sldb:
  by: agent
  at: '2026-11-15T16:51:04Z'
  authority: generated
  via: create_document
id: task-espejo-sldb-sldb-mcp-servidor-mcp-genérico-a
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

# Espejo sldb: sldb mcp servidor MCP genérico (A)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de una tarea del desk de sldb, para que depends_on la exprese con un id local que deskops resuelve; el trabajo vive en sldb.

## Goal

_Describe the concrete result this task must produce._

Disponer de sldb mcp (servidor MCP genérico con niveles, propose/apply, log de señales y punto de extensión) para que specIR monte sus tools de dominio encima.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado de la tarea de sldb task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e (desk de sldb, repo registrado como sldb). Fuera: cualquier trabajo en IR; el cambio se pide y se cierra en el desk de sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando la tarea de sldb task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e está cerrada, con un commit de sldb como evidencia externa.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

La tarea de sldb task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e está cerrada y integrada en la rama principal de sldb.
