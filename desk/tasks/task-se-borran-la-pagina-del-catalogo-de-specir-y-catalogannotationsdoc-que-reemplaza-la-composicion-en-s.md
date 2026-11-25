---
sldb:
  by: agent
  at: '2026-11-25T22:54:47Z'
  authority: generated
  via: create_document
id: task-se-borran-la-pagina-del-catalogo-de-specir-y-catalogannotationsdoc-que-reemplaza-la-composicion-en-s
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-specir-install-siembra-la-composicion-de-la-pantalla-del-catalogo-como-documento-del-store
pills: []
files: []
pointers: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# se borran la página del catálogo de specIR y CatalogAnnotationsDoc, que reemplaza la composición en surface

## Rationale

_Explain why this task exists or the business driver behind it._

BLOQUEADA hasta que exista la composición del catálogo en surface y la exportación de una composición entera (pedidos en los inbox de sldb y de graph_ui del 2026-11-25). Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo R4. src/specir/visual/catalog/ son 1.054 líneas que arman una página HTML: specIR no dibuja.

## Goal

_Describe the concrete result this task must produce._

Que el catálogo se vea y se exporte solo desde surface.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/visual/catalog/, el comando specir catalog build, CatalogAnnotationsDoc, sus pruebas y recursos. Fuera: el catálogo como datos (qué diagramas hay y en qué categoría), que se queda; y las anotaciones ya guardadas, que no se borran sin decir a dónde pasan.

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de borrar, comprobar que la composición muestra lo mismo que la página y que se puede exportar. Decir qué pasa con las anotaciones existentes de CatalogAnnotationsDoc: se migran a las anotaciones del editor o se informa a JP.

## Validation

_List the checks required before this task can close._

- ! test -e src/specir/visual/catalog
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

No existe src/specir/visual/catalog/, specir no ofrece catalog build y dice dónde se ve el catálogo, ninguna anotación guardada se pierde, y la suite pasa.
