FILE:desk/tasks/task-specir-install-siembra-la-notacion-de-capas-de-specir-y-una-vista-del-blog-de-ejemplo-sale-con-un-gl.md
---
sldb:
  by: agent
  at: '2026-11-25T17:45:06Z'
  authority: generated
  via: create_document
id: task-specir-install-siembra-la-notacion-de-capas-de-specir-y-una-vista-del-blog-de-ejemplo-sale-con-un-gl
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

# specir install siembra la notación de capas de specIR y una vista del blog de ejemplo sale con un glifo por nodo

## Rationale

_Explain why this task exists or the business driver behind it._

docs/decisiones/paridad-por-capacidades.md (JP, 2026-11-25): specIR declara y graph_ui dibuja. Los 11 tipos de dominio de specIR no tienen notación en el store, así que lo extraído del código no se puede ver. Hay un borrador validado en desk/drawer/plans/paridad-por-capacidades/specir-layers.yml (11 glifos, 11 links).

## Goal

_Describe the concrete result this task must produce._

Que instalar specIR en un store deje la notación de capas lista para que una ViewDoc la use.

## Scope

_State what is in scope and what is out of scope._

Dentro: los datos de notación de specIR y src/specir/install.py. Fuera: carriles por capa (dependen de una tarea de graph_ui), ORCA e IFML.

## Implementation Path

_Outline the expected implementation route or affected surface._

Partir del borrador del drawer. La notación es dato sembrado, igual que relation_types.yaml y rules.yaml.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_install.py tests/test_layers_notation.py

## Done When

_Name the observable condition that makes the task complete._

En un store nuevo con specir install y el blog de ejemplo extraído, sldb notations validate acepta la notación y resolver una vista con ella devuelve cada documento de dominio con su glifo y cada relación con su link, sin huecos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-specir-install-siembra-la-notacion-de-capas-de-specir-y-una-vista-del-blog-de-ejemplo-sale-con-un-gl: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

