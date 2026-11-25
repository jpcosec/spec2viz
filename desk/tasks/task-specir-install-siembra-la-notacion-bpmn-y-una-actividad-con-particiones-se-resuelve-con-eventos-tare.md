---
sldb:
  by: agent
  at: '2026-11-25T22:47:07Z'
  authority: generated
  via: create_document
id: task-specir-install-siembra-la-notacion-bpmn-y-una-actividad-con-particiones-se-resuelve-con-eventos-tare
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-specir-es-dueno-de-las-notaciones-de-uml-y-de-las-clases-de-spec-por-tipo-de-diagrama-las-siembra-sp
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# specir install siembra la notación BPMN, y una actividad con particiones se resuelve con eventos, tareas, compuertas y carriles sin huecos

## Rationale

_Explain why this task exists or the business driver behind it._

Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo N3. BPMN es un estándar, y un estándar es una notación: contenido de specIR. Hoy BPMN existe en specIR solo como exporte a XML (src/specir/visual/renderers/bpmn.py); no hay una notación con la que el editor de grafo dibuje un proceso. sldb ya acepta carriles por partición en el layout de una NotationDoc y graph_ui ya los dibuja.

## Goal

_Describe the concrete result this task must produce._

Que un proceso guardado como actividad se vea en el editor de grafo con la notación BPMN, declarada como dato.

## Scope

_State what is in scope and what is out of scope._

Dentro: el documento de notación BPMN y sus glifos, como semilla de specIR; lo que specir install necesite para sembrarla; pruebas. Fuera: tocar sldb o graph_ui (lo que falte se pide por su inbox), código por notación en cualquier parte, y el exporte a BPMN XML, que se queda como está.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer sldb/docs/architecture/notations-and-views.md y cómo quedaron las notaciones de UML al mudarse a specIR. La notación declara que implementa BPMN 2.0 si sldb ya permite declarar el estándar; si no, se deja anotado. Carriles con el layout de particiones. Reusar la paleta de bpmn_palette.py solo como referencia de formas.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/notations/test_bpmn_notation.py

## Done When

_Name the observable condition that makes the task complete._

Después de specir install, el store tiene la notación BPMN. Una actividad de tests/visual/fixtures con evento de inicio, evento de fin, tareas, una compuerta y dos particiones se resuelve con esa notación: cada nodo recibe un glifo distinto según su clase, las particiones salen como carriles y la vista resuelta no informa ningún documento sin glifo. La misma actividad se sigue resolviendo con la notación de actividad de UML.
