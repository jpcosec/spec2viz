---
sldb:
  by: agent
  at: '2026-11-25T22:53:45Z'
  authority: generated
  via: create_document
id: task-specir-install-siembra-la-composicion-de-la-pantalla-del-catalogo-como-documento-del-store
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# specir install siembra la composición de la pantalla del catálogo como documento del store

## Rationale

_Explain why this task exists or the business driver behind it._

BLOQUEADA hasta que sldb/surface defina cómo se declara una composición (pedido en el inbox de sldb del 2026-11-25, "surface: un plugin declara como dato la composición de una pantalla"). Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo S5. JP decidió que el plugin aporta como dato la composición de su pantalla: lista de diagramas por categoría, editor de grafo y editor de texto con el documento del nodo seleccionado.

## Goal

_Describe the concrete result this task must produce._

Que la pantalla del catálogo de specIR exista como dato que surface arma, sin interfaz en specIR.

## Scope

_State what is in scope and what is out of scope._

Dentro: el documento de composición como semilla y su siembra. Fuera: componentes, estilos, o cualquier código de interfaz; el formato de la composición, que lo define surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

Empezar leyendo la respuesta de sldb al pedido. Si surface todavía no tiene compositor, la tarea no se empieza.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_catalog_composition.py

## Done When

_Name the observable condition that makes the task complete._

Después de specir install el store tiene la composición del catálogo, válida contra el modelo que defina surface, y surface abre con ella la lista por categoría, el diagrama elegido y el documento del nodo seleccionado.
