---
sldb:
  by: agent
  at: '2026-11-17T00:17:41Z'
  authority: generated
  via: save_document_payload
id: task-espejo-sldb-sldb-api-expone-los-facts-de-código-que-necesitan-los-extractores-c1-c5
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- ../sldb/desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
- runs/subagents/deskops-e-67da42f92e6d/result-summary.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Espejo sldb: sldb.api expone los facts de código que necesitan los extractores (C1–C5)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de un trabajo del desk de sldb, para que depends_on lo exprese con un id local que deskops resuelve. El trabajo vive en sldb. El ejecutor de IR08 (runs/subagents/deskops-e-67da42f92e6d) midió que B2 lee TS, TSX, JS, JSX y SQL de Postgres, pero sldb.api no expone los facts: no hay listado público de facts por archivo (C1), ni span y hash (C2), ni facts de Django/DRF (C3), ni claves del SQL (C4), y write_anchor no es público (C5).

## Goal

_Describe the concrete result this task must produce._

Que sldb.api exponga los facts de código con sus anclas, span y hash, incluidos los de Django/DRF y las claves del SQL de Postgres, para que specIR mapee sin leer código.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado del trabajo de sldb pedido en la nota de su inbox 20261116-211648 (repo registrado como sldb). Cuando sldb cree su tarea, su id se agrega a las referencias de este espejo. Fuera: cualquier trabajo en IR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando sldb cierre el trabajo con commits en origin main de sldb como evidencia externa, o cuando JP decida otro reparto.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

sldb.api expone C1 a C4 (y C5, o una alternativa pública para escribir anclas), con el trabajo cerrado e integrado en origin main de sldb.
