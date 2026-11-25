---
sldb:
  by: agent
  at: '2026-11-25T01:09:45Z'
  authority: generated
  via: create_document
id: task-plan-probar-uis-con-graph-ui-como-diccionario-de-componentes-y-una-forma-comoda-de-usar-specir-ahi
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Plan: probar UIs con graph_ui como diccionario de componentes y una forma comoda de usar specIR ahi

## Rationale

_Explain why this task exists or the business driver behind it._

JP 2026-11-24: testear UI usando graph_ui (UIs/graph_ui, jpcosec/graph_ui: editor visual de una KB SLDB, React/htm, con auto_user_test) como diccionario de componentes; hay que disenar una forma comoda de usar specIR ahi. specIR ya modela la capa UX (extractor React TSX: controles, acciones, triggers e invokes hacia operaciones API).

## Goal

_Describe the concrete result this task must produce._

Un plan en desk/drawer/plans/graph-ui-diccionario-de-componentes/ que diga: que es el diccionario de componentes (que componente de graph_ui es que nodo de la capa UX de specIR), como se genera (extractor React de specIR sobre graph_ui), como se usa para probar UIs (que prueba lee el diccionario: auto_user_test, flujos, controles esperados), la ergonomia (comando o tool MCP de specIR), y el DAG de tareas chicas con depends_on para implementarlo. Decisiones abiertas como task.decision para JP.

## Scope

_State what is in scope and what is out of scope._

Solo el plan (documentos en el drawer de IR). Leer UIs/graph_ui (README, DESIGN, auto_user_test, src), src/specir/extract/react_tsx.py y models/domain.py. Fuera: codigo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario de componentes de graph_ui y de lo que auto_user_test ya prueba. 2) Correr el extractor React de specIR sobre graph_ui en un store temporal bajo /mnt/ssd/tmp/sldb1 y anotar que sale y que falta. 3) Proponer el formato del diccionario y la ergonomia. 4) DAG de tareas chicas (cada una cabe en menos de 2 h, con sus tests). 5) Decisiones para JP.

## Validation

_List the checks required before this task can close._

- ls desk/drawer/plans/graph-ui-diccionario-de-componentes/

## Done When

_Name the observable condition that makes the task complete._

El plan existe en el drawer con inventario, resultado real del extractor sobre graph_ui, propuesta de diccionario y de ergonomia, DAG de tareas y decisiones abiertas.
