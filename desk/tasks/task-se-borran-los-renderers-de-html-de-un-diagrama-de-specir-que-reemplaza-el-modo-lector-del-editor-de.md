---
sldb:
  by: agent
  at: '2026-11-25T22:51:24Z'
  authority: generated
  via: create_document
id: task-se-borran-los-renderers-de-html-de-un-diagrama-de-specir-que-reemplaza-el-modo-lector-del-editor-de
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# se borran los renderers de HTML de un diagrama de specIR, que reemplaza el modo lector del editor de grafo

## Rationale

_Explain why this task exists or the business driver behind it._

BLOQUEADA hasta que graph_ui cierre el SVG y el HTML autocontenido del modo lector (sus tareas G-B1 y G-B2). Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo R3. specIR no dibuja. bpmn_viewer.py, graph_html.py, tree.py y antonia_html.py de src/specir/visual/renderers/ suman 1.007 líneas que hacen lo que hará el modo lector.

## Goal

_Describe the concrete result this task must produce._

Que el HTML de un diagrama salga solo del editor de grafo.

## Scope

_State what is in scope and what is out of scope._

Dentro: esos cuatro renderers, su registro en renderers/__init__.py, las opciones de render que los nombran, sus pruebas y recursos. Fuera: los exportes de texto y la página del catálogo.

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de borrar, comprobar con un diagrama de cada tipo que el modo lector de graph_ui lo exporta. Lo que el modo lector no cubra se informa a graph_ui por su inbox y ese renderer no se borra todavía.

## Validation

_List the checks required before this task can close._

- ! ls src/specir/visual/renderers/bpmn_viewer.py src/specir/visual/renderers/graph_html.py src/specir/visual/renderers/tree.py src/specir/visual/renderers/antonia_html.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Los cuatro archivos no existen, specir diagram render ya no ofrece esos formatos y dice dónde se obtienen, y la suite pasa. La skill y el README no los nombran.
