---
id: task-from-graph-etiqueta-y-estilo-desde-campos-del-documento
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

# from-graph: etiqueta y estilo desde campos del documento

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261021-125038-suggestion-from-graph-etiqueta-y-estilo-desde-campos-del-documento.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261021-125038-suggestion-from-graph-etiqueta-y-estilo-desde-campos-del-documento.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Requisito desde Governance (DAG de repos, 2026-10-21). 'spec2viz diagram from-graph --store .sldb --model RepositoryDoc --relation depends_on' usa como label el id del documento (repo-chatbot-infra) y como kind el modelo (RepositoryDoc). Falta poder elegir un campo para el label (name/title) y otro para el kind o el estilo (status o una etiqueta como system:<id>), para colorear los repos por sistema o por estado sin editar el spec generado. También agrupar por un campo (contains por etiqueta) ayudaría.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
