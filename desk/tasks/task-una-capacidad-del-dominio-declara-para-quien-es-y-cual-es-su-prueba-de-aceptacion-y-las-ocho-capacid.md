---
sldb:
  by: agent
  at: '2026-11-25T19:12:59Z'
  authority: generated
  via: create_document
id: task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# una capacidad del dominio declara para quién es y cuál es su prueba de aceptación, y las ocho capacidades de specIR quedan cargadas así en su store

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md y docs/decisiones/paridad-por-capacidades.md (JP, 2026-11-25): specIR cumple capacidades, y qué tiene que poder hacer un sistema, para quién, es de specIR. DomainOperationDoc ya se define como "una capacidad del dominio, independiente de cómo se invoca", pero no dice para quién es ni qué prueba la acredita. Si se cumple no es un campo: lo dice su prueba.

## Goal

_Describe the concrete result this task must produce._

Que una capacidad sea un nodo de specIR con destinatario y con su prueba de aceptación enlazada, y que una regla exija esa prueba.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/models/domain.py, data/rules.yaml, y las ocho capacidades de la tabla de docs/decisiones/paridad-por-capacidades.md como datos. Fuera: un campo de estado cumplida o no cumplida, capacidades de otros repos.

## Implementation Path

_Outline the expected implementation route or affected surface._

Reemplaza al trabajo "capacidades como datos del store" del plan desk/drawer/plans/paridad-por-capacidades/. El enlace a la prueba usa lo que ya existe para materializaciones y anclas de código; no se crea otro mecanismo.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_capabilities_as_nodes.py

## Done When

_Name the observable condition that makes the task complete._

Las ocho capacidades están en el store de specIR, cada una con su destinatario. Una capacidad sin prueba de aceptación la informa la regla. Las que ya tienen prueba (7 y 8) la enlazan y su ancla está intacta. Una vista las lista con su prueba.
