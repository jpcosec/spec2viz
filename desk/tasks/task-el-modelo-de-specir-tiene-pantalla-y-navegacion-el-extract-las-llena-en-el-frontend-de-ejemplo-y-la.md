---
sldb:
  by: agent
  at: '2026-11-25T22:48:10Z'
  authority: generated
  via: create_document
id: task-el-modelo-de-specir-tiene-pantalla-y-navegacion-el-extract-las-llena-en-el-frontend-de-ejemplo-y-la
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-specir-es-dueno-de-las-notaciones-de-uml-y-de-las-clases-de-spec-por-tipo-de-diagrama-las-siembra-sp
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# el modelo de specIR tiene pantalla y navegación, el extract las llena en el frontend de ejemplo y la notación IFML las muestra

## Rationale

_Explain why this task exists or the business driver behind it._

Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo N4. Los tipos de interfaz de src/specir/models/domain.py son control, acción y campo. No hay dónde decir en qué pantalla está un control ni a qué pantalla lleva una acción, y sin eso no se puede declarar IFML ni recorrer una interfaz para probarla.

## Goal

_Describe the concrete result this task must produce._

Que specIR describa una interfaz como pantallas que contienen controles y acciones que navegan entre pantallas.

## Scope

_State what is in scope and what is out of scope._

Dentro: un tipo de nodo de pantalla en la capa de interfaz; los tipos de relación de pertenencia y de navegación en data/relation_types.yaml; la regla de que un control pertenece a una pantalla; el mapeo en extract/ para React con rutas; la notación IFML como semilla. Fuera: leer código (los hechos los da sldb; si falta uno se pide por el inbox de sldb), ORCA, y el diccionario de controles.

## Implementation Path

_Outline the expected implementation route or affected surface._

Proponer desde lo que debería ser, no desde lo que hay: primero los tipos y relaciones, después el mapeo. Antes de crear un tipo de relación nuevo, revisar si uno de los diez existentes ya lo dice. IFML se declara como notación (contenedor de vista, componente de vista, evento, flujo de navegación), sin código por notación.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/models/test_screens_and_navigation.py tests/extract/test_frontend_extraction.py
- python -m pytest -q tests/notations/test_ifml_notation.py

## Done When

_Name the observable condition that makes the task complete._

Sobre tests/fixtures/blog_frontend, el extract deja un nodo por pantalla, cada control con su relación a una sola pantalla, y cada acción que cambia de ruta con su relación a la pantalla de destino. Un control sin pantalla lo informa la regla. Una vista con la notación IFML se resuelve sin documentos sin glifo. Los nodos nuevos llevan origen y verificación como los demás.
