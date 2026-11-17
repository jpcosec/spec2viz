---
sldb:
  by: agent
  at: '2026-11-17T03:08:44Z'
  authority: generated
  via: save_document_payload
id: task-espejo-sldb-sldb-mcp-sirve-undo-changes-con-la-pila-de-lotes-inversos-de-la-sesión
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
- task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Espejo sldb: sldb mcp sirve undo_changes con la pila de lotes inversos de la sesión

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de un trabajo del desk de sldb, para que depends_on lo exprese con un id local. sldb respondió en la nota de inbox 20261116-232335 que undo_changes lo sirve sldb mcp: apply_changes apila report.inverse en una pila por sesión, en memoria, y undo_changes(steps) deshace con guardas. Está como tarea en sldb.

## Goal

_Describe the concrete result this task must produce._

Que sldb mcp sirva undo_changes, para que IR04b lo verifique desde specIR.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado de la tarea de sldb task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi. Fuera: cualquier trabajo en IR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando la tarea de sldb esté cerrada e integrada en origin main de sldb, con sus commits como evidencia externa.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

La tarea de sldb task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi está cerrada y sus commits están en origin main de sldb.
