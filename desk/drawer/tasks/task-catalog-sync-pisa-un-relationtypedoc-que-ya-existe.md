---
id: task-catalog-sync-pisa-un-relationtypedoc-que-ya-existe
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

# catalog sync pisa un RelationTypeDoc que ya existe

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261021-125040-unclear-catalog-sync-pisa-un-relationtypedoc-que-ya-existe.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261021-125040-unclear-catalog-sync-pisa-un-relationtypedoc-que-ya-existe.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desde Governance (2026-10-21): creé sldb/relation_types/depends_on.md con 'sldb doc add --model RelationTypeDoc' (source_types y target_types = [RepositoryDoc], descripción propia). 'spec2viz catalog sync' sobre un spec con aristas depends_on lo reescribió: by spec2viz, tipos vacíos y descripción genérica. Después, sldb stores check marcó store/data-mutation. Esperado: si el tipo ya existe, reusarlo sin reescribirlo (o fallar si las aristas del spec no cumplen sus source_types/target_types). Una segunda sync, ya con tipos vacíos, no lo volvió a tocar.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
