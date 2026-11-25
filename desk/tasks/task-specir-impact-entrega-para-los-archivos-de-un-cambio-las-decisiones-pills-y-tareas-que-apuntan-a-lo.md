---
sldb:
  by: agent
  at: '2026-11-25T19:29:42Z'
  authority: generated
  via: save_document_payload
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

Aclaraciones de la revisión: va después de la tarea de sldb (task-sldb-responde-que-documentos-aplican-...) y de la de punteros de deskops; parte de main con ambas integradas. La operación de sldb es la de esa tarea (nombre canónico anchors_resolve o el que quede en sldb/docs/architecture/command-taxonomy.md), vía sldb.api, sin copiarla. Otros stores = los .sldb de los desks de /mnt/ssd/proyectos/SLDB_1/{deskops,sldb,UIs/graph_ui,IR}, más los que se pasen con --store (repetible). Categoría = tag; via es 'direct' o 'tag:<tag>' tal como lo devuelve sldb. Capa = la capa del nodo de specIR (la que asigna el extractor); una tarea apunta a la capa si su campo pointers tiene 'tag:<capa>'. Archivo→nodo: por el ancla de código del nodo (ruta del archivo del que salió). Tipos incluidos: AtomAdrDoc (decisiones), PillDoc y sus subtipos, y TaskDoc y sus subtipos. Salida: lista de {doc, model, via, node} ordenada por doc; archivo sin nodos = lista vacía, rc 0. Herramienta MCP: specir_impact en el mcp_extension de specIR, mismo contrato que el comando 'specir impact <archivos...>'. La propuesta de deskops (desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/) es contexto, no norma. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_impact_reaches_work_documents.py

## Done When

_Name the observable condition that makes the task complete._

Con un store de prueba donde una decisión apunta a un nodo y una tarea apunta a la capa de ese nodo, pedir el impacto del archivo del que salió el nodo devuelve el nodo, la decisión y la tarea, y dice si llegó directo o por categoría. Un archivo sin nodos devuelve vacío sin error.
