---
id: task-atributos-de-arista-en-la-vista-multiplicidades-acciones-de-transicion-y-fragmentos-de-secuencia-car
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
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

# Atributos de arista en la vista: multiplicidades, acciones de transicion y fragmentos de secuencia; carriles y grilla con graph_ui

## Rationale

_Explain why this task exists or the business driver behind it._

El contrato de notacion (docs/notation-contract.md #8) deja fuera lo que RelationDoc no puede llevar: multiplicidades y roles de una relacion de clases, la accion de una transicion y el group de los mensajes de secuencia. graph_ui dibuja lanes y grid como grafo con aviso porque la vista no fija como ordenarlos.

## Goal

_Describe the concrete result this task must produce._

Cada arista del spec conserva sus atributos en el store (campo libre de RelationDoc pedido a sldb-04, o alternativa acordada), resolve_view los expone (link.data, source_label/target_label en LinkDoc, fragments de secuencia por group) y el contrato fija como se ordenan carriles (participantes) y grilla (etapas por data.order, filas por nest). graph_ui los consume.

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/sldb_sync.py (atributos de arista), spec2viz/sldb_models.py (LinkDoc.source_label/target_label), spec2viz/notations/uml-class.yml y statechart.yml y uml-sequence.yml, spec2viz/notation_view.py (data, fragments, orden de carriles y grilla), tests, docs/notation-contract.md. OUT: el dibujo en graph_ui; cambios dentro de sldb (los pide, no los hace).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_notation_view.py tests/test_sldb_sync.py -q

## Done When

_Name the observable condition that makes the task complete._

resolve_view de class.sldb-models trae multiplicidades en los extremos; el statechart trae action; sequence.render-pipeline trae fragments cuando hay group; tests verdes; contrato actualizado; graph-ui-59 confirma que lee lanes/grid con el orden fijado.
