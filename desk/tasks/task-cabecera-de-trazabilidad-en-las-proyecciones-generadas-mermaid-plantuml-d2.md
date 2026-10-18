---
id: task-cabecera-de-trazabilidad-en-las-proyecciones-generadas-mermaid-plantuml-d2
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-spec2viz-migration-and-spec-provenance.md
---

# Cabecera de trazabilidad en las proyecciones generadas (Mermaid, PlantUML, D2)

## Rationale

_Explain why this task exists or the business driver behind it._

Del drawer task-spec2viz-migration-and-spec-provenance: una proyeccion generada debe decir de que spec sale y como se valida, para que nadie la edite a mano. La otra mitad del drawer, 'spec2viz import mermaid', queda obsoleta: no hay Mermaid hecho a mano en el repo y la importacion desde datos ya existe como diagram from-graph sobre el store.

## Goal

_Describe the concrete result this task must produce._

diagram render antepone a cada salida de texto una linea de comentario con la ruta del spec y el comando de validacion, en la sintaxis de comentario del renderer (%% en Mermaid, ' en PlantUML, # en D2); los goldens y el lint de Mermaid siguen en verde.

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/__init__.py (render_to_file), tests, goldens de examples/ y docs/architecture/spec2viz/*.mmd regenerados, CHANGELOG. OUT: spec2viz import mermaid (obsoleto, ver why); salidas no textuales (vega json, html).

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py tests/test_renderers.py -q

## Done When

_Name the observable condition that makes the task complete._

Una proyeccion .mmd/.puml/.d2 recien renderizada empieza por la cabecera de trazabilidad; spec2viz diagram lint acepta los .mmd con cabecera; pytest verde.
