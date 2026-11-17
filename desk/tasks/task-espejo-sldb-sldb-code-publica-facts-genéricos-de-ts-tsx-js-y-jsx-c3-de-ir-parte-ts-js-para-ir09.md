---
sldb:
  by: agent
  at: '2026-11-17T11:10:39Z'
  authority: generated
  via: save_document_payload
id: task-espejo-sldb-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-c3-de-ir-parte-ts-js-para-ir09
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- ../sldb/desk/tasks/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam.md
- ../sldb/desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
- task-espejo-sldb-sldb-api-expone-los-facts-de-código-que-necesitan-los-extractores-c1-c5
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Espejo sldb: sldb.code publica facts genéricos de TS, TSX, JS y JSX (C3 de IR, parte TS/JS, para IR09)

## Rationale

_Explain why this task exists or the business driver behind it._

Espejo en el desk de IR de la tarea de sldb task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam. Sale del espejo C1–C5, que se cierra con C1, C2, C3 Python, C4 y C5 ya en origin main de sldb; la parte TS/JS de C3 sigue abierta en sldb y es la que bloquea IR09.

## Goal

_Describe the concrete result this task must produce._

Que sldb.api.code.code_facts dé, para TS, TSX, JS y JSX, las llamadas de cada función, componente o hook (fetch, axios, clientes de API y otros símbolos) con su primer argumento literal, y los atributos JSX que ligan un evento a un handler, para que specIR arme los contratos de API de React sin leer código.

## Scope

_State what is in scope and what is out of scope._

Dentro: reflejar el estado de la tarea de sldb task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam (nota de origen 20261116-211648 en el inbox de sldb). Fuera: cualquier trabajo en IR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin implementación en IR. Se cierra cuando sldb cierre su tarea con commits de código y closeout en origin main de sldb como evidencia externa, o cuando JP decida otro reparto.

## Validation

_List the checks required before this task can close._

- git -C ../sldb merge-base --is-ancestor <closeout de la tarea de sldb> origin/main sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

La tarea de sldb está cerrada y su código y closeout están en origin main de sldb.
