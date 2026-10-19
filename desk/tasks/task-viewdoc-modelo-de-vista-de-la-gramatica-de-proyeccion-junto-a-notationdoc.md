---
id: task-viewdoc-modelo-de-vista-de-la-gramatica-de-proyeccion-junto-a-notationdoc
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- 218676d
- tests/test_view_doc.py
- desk/atoms/atom-viewdoc-vista-portable-de-la-gramatica-de-proyeccion.md
depends_on: []
pills: []
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# ViewDoc: modelo de vista de la gramatica de proyeccion junto a NotationDoc

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de graph_ui (2026-10-19), decision del coordinador SLDB_1: las vistas de la gramatica de proyeccion son documentos del store y su modelo vive en spec2viz junto a NotationDoc (PROJECTION_GRAMMAR_SPEC.md §3 de graph_ui).

## Goal

_Describe the concrete result this task must produce._

spec2viz.sldb_models.ViewDoc con nodes {model, where}, relations, direction, notation opcional, layout override y description; portable; registrado con los demas modelos de spec2viz; layout.style y ring_field reconocidos.

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/sldb_models.py, sldb_sync.MODEL_REFS, notation.py (layout.style), tests/test_view_doc.py, docs/notation-contract.md §12, CHANGELOG. OUT: sync o CLI de vistas; evaluacion (graph_ui).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_view_doc.py -q

## Done When

_Name the observable condition that makes the task complete._

tests/test_view_doc.py en verde contra un store real; ViewDoc referencia su NotationDoc en el indice de aristas.
