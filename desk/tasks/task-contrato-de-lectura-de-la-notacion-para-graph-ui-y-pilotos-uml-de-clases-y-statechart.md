---
id: task-contrato-de-lectura-de-la-notacion-para-graph-ui-y-pilotos-uml-de-clases-y-statechart
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references: []
depends_on:
- task-vocabulario-visual-declarativo-notationdoc-glyphdoc-y-linkdoc-sincronizados-al-store
pills:
- desk/contexts/pill-adr-spec2viz-es-dueño-del-vocabulario-visual-graph-ui-de-la-vista-generica-y-los-gestos.md
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Contrato de lectura de la notacion para graph_ui y pilotos UML de clases y statechart

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui necesita saber como resolver SpecDoc -> NotationDoc -> GlyphDoc/LinkDoc contra los documentos del store para dibujar sin inferir del payload. Sin contrato escrito la vista generica de graph_ui y la sincronizacion de spec2viz derivan.

## Goal

_Describe the concrete result this task must produce._

Un documento de contrato en spec2viz (docs/notation-contract.md) que fija: como se elige la notacion de un spec, como casa un glifo (model + where, primer match en orden), como casa un link (relation_type del RelationDoc; contains como arista nest), las plantillas de rotulo {campo} sobre el payload de SpecNodeDoc, y la aplicabilidad (modelos y relaciones que nombra la notacion existen en el store). Los dos pilotos sincronizados en el store del repo y visibles en graph_ui /api/graph; la D3 del plan de cierre de graph_ui apuntando a este contrato.

## Scope

_State what is in scope and what is out of scope._

IN: docs/notation-contract.md, specs piloto class y state en docs/architecture/spec2viz (los que ya existen o uno nuevo por tipo si falta), sync al store, verificacion con graph_ui (SLDB_STORE=spec2viz/.sldb) via graph-ui-59, mensaje a graph-ui-59 con el contrato. OUT: implementar la vista generica (graph_ui), gestos, edit-back.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Escribir el contrato a partir de los modelos ya sincronizados. 2) Asegurar un spec class y un spec state en el repo con notacion asignada. 3) Pedir a graph-ui-59 que levante serve.py sobre el store de spec2viz y confirme que /api/graph y /api/schema listan NotationDoc/GlyphDoc/LinkDoc. 4) Registrar en el contrato lo que graph_ui pida cambiar.

## Validation

_List the checks required before this task can close._

- spec2viz diagram sync docs/architecture/spec2viz/*.yml --strict
- sldb edges check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

docs/notation-contract.md commiteado; graph-ui-59 confirma lectura de los documentos de notacion desde su /api; sldb edges check OK sobre el store de spec2viz.
