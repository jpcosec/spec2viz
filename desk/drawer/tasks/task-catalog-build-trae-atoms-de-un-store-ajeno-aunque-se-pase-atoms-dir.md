---
id: task-catalog-build-trae-atoms-de-un-store-ajeno-aunque-se-pase-atoms-dir
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# catalog build trae atoms de un store ajeno aunque se pase --atoms-dir

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261022-002802-suggestion-catalog-build-trae-atoms-de-un-store-ajeno-aunque-se-pase-atoms-dir.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261022-002802-suggestion-catalog-build-trae-atoms-de-un-store-ajeno-aunque-se-pase-atoms-dir.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

catalog build: --atoms-dir no manda. _raw_atoms_by_view (spec2viz/deskops.py) primero llama a SldbAtomResolver().build_atoms_by_view(items) y solo usa --atoms-dir como respaldo para las vistas que quedan vacías. Corrido desde labchile_chatbots/docs/spec2viz con '--atoms-dir ../../desk/atoms', el resolver trae 146 atoms del store de deskops (SLDB_1/deskops/desk/atoms, p. ej. atom-agents-read-by-decision-need) en vez de los 3 del repo. Esperado: si se pasa --atoms-dir, que mande ese directorio (o el store del repo del catálogo), nunca un store ajeno. Repro: cd labchile_chatbots/docs/spec2viz && spec2viz catalog build --config catalog.yml --out /tmp/c.html --atoms-dir ../../desk/atoms; contar window.ATOMS_DB. labchile dejó build/catalog.html sin regenerar por esto (inbox de labchile, 2026-10-22).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
