---
id: task-activity-el-paso-de-start-no-puede-volverse-el-nodo-inicial
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
- d256c48
- tests/test_sldb_sync.py::test_activity_start_on_a_decision_keeps_its_diamond
- 'verificado en graph_ui a 1800x1200: capturas en ~/.cache/spec2viz-issues/20261019-visual/verified-fbb37ea'
depends_on: []
pills: []
files: []
task_type: bug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Activity: el paso de start no puede volverse el nodo inicial

## Rationale

_Explain why this task exists or the business driver behind it._

Reporte visual del 2026-10-19 (capturas en ~/.cache/spec2viz-issues/20261019-visual/): el paso nombrado en start: se marca initial y la notacion lo dibuja como el circulo negro; su rotulo queda suelto y, si es una decision, el rombo desaparece.

## Goal

_Describe the concrete result this task must produce._

diagram sync crea un nodo inicial propio que fluye por next al paso de start, como el nodo final; el paso de start conserva su glifo (accion o decision).

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/sldb_sync.py (spec_elements, _activity_edges), tests, pilotos sincronizados del repo. OUT: graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_activity_lanes.py tests/test_notation_view.py -q

## Done When

_Name the observable condition that makes the task complete._

Un spec con start en una decision se ve con circulo inicial, flecha y rombo con su rotulo en graph_ui a 1800x1200; tests en verde.
