---
sldb:
  by: agent
  at: '2026-11-25T19:13:06Z'
  authority: generated
  via: create_document
id: task-specir-impact-entrega-para-los-archivos-de-un-cambio-las-decisiones-pills-y-tareas-que-apuntan-a-lo
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

# specir impact entrega, para los archivos de un cambio, las decisiones, pills y tareas que apuntan a lo afectado

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): el contexto que se le entrega a quien ejecuta un trabajo (qué leer y qué respetar) no debería escribirse a mano en una pill. specIR ya calcula a qué nodos alcanza un cambio (src/specir/impact.py, sobre graph_path de sldb), pero su respuesta se queda en los nodos del sistema y no llega a los documentos de trabajo que apuntan a ellos.

## Goal

_Describe the concrete result this task must produce._

Que el impacto de un cambio incluya los documentos de otros stores que apuntan a los nodos afectados, con la vía por la que llega cada uno.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/impact.py y su herramienta MCP. Fuera: escribir pills, decidir qué se hace con la respuesta (es de deskops).

## Implementation Path

_Outline the expected implementation route or affected surface._

Usa la operación de sldb que responde qué documentos aplican a un archivo o símbolo; no recorre el grafo por su cuenta. Sigue siendo de solo lectura.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_impact_reaches_work_documents.py

## Done When

_Name the observable condition that makes the task complete._

Con un store de prueba donde una decisión apunta a un nodo y una tarea apunta a la capa de ese nodo, pedir el impacto del archivo del que salió el nodo devuelve el nodo, la decisión y la tarea, y dice si llegó directo o por categoría. Un archivo sin nodos devuelve vacío sin error.
