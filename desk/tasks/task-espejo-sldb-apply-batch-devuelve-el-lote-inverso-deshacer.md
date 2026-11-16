---
sldb:
  by: agent
  at: '2026-11-16T05:05:00Z'
  authority: generated
  via: save_document_payload
id: task-espejo-sldb-apply-batch-devuelve-el-lote-inverso-deshacer
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

# Espejo sldb: apply_batch devuelve el lote inverso (deshacer)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de una tarea del desk de sldb, para que depends_on la exprese con un id local que deskops resuelve; el trabajo vive en sldb.

## Goal

_Describe the concrete result this task must produce._

Disponer en sldb del lote inverso con guardas en el resultado de apply_batch, base del deshacer por MCP.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado de la tarea de sldb task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855 (desk de sldb, repo registrado como sldb). Fuera: cualquier trabajo en IR; el cambio se pide y se cierra en el desk de sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando la tarea de sldb task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855 está cerrada, con un commit de sldb como evidencia externa.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

La tarea de sldb task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855 está cerrada y integrada en la rama principal de sldb.
