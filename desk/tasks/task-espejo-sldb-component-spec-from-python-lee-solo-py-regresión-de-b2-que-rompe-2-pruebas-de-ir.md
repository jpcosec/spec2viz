---
sldb:
  by: agent
  at: '2026-11-17T03:08:52Z'
  authority: generated
  via: save_document_payload
id: task-espejo-sldb-component-spec-from-python-lee-solo-py-regresión-de-b2-que-rompe-2-pruebas-de-ir
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
- task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone
- runs/subagents/deskops-t-270be4709340/result-summary.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Espejo sldb: component_spec_from_python lee solo .py (regresión de B2 que rompe 2 pruebas de IR)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de un trabajo del desk de sldb. Desde sldb 600b51a9, component_spec_from_python recorre el .js minificado vendorizado de IR y rompe tests/visual/test_sync_generation_parity.py (2 pruebas). La suite completa de IR no da verde mientras siga así. sldb respondió en la nota de inbox 20261116-232335 que va a leer solo .py; está como tarea en sldb.

## Goal

_Describe the concrete result this task must produce._

Que la suite completa de IR vuelva a verde sin exclusiones del lado de IR.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado de la tarea de sldb task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone. Fuera: cualquier trabajo en IR; excluir archivos en IR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando la tarea de sldb esté cerrada e integrada en origin main de sldb, y las 2 pruebas de test_sync_generation_parity pasen contra ese sldb.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

La tarea de sldb task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone está cerrada en origin main de sldb y tests/visual/test_sync_generation_parity.py pasa en IR.
