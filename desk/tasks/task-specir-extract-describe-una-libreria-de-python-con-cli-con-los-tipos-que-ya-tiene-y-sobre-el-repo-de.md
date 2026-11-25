---
sldb:
  by: agent
  at: '2026-11-25T19:21:06Z'
  authority: generated
  via: create_document
id: task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de
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

# specir extract describe una librería de Python con CLI con los tipos que ya tiene, y sobre el repo deskops deja sus comandos, operaciones y modelos como nodos con capa

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): el qué y el dónde de un sistema son de specIR. Sus extractores cubren hoy una aplicación web (src/specir/extract/: django_drf, react_tsx, routes, sql), así que no describe a sldb, deskops ni a sí mismo. Nada lo impide: sldb ya entrega los hechos de código de Python (sldb/src/sldb/code/: py_module, py_calls, imports) y los tipos de specIR ya contemplan el caso, porque DomainOperationDoc se define como una capacidad "independent of how it is invoked (UI, CLI, job, agent)". Falta el extractor.

## Goal

_Describe the concrete result this task must produce._

Un extractor más, al lado de los que existen, que lee los hechos de Python de sldb y produce nodos de los tipos actuales: un comando de CLI como control y acción de interfaz, una función de la API pública como operación de API, lo que ejecuta como handler y operación de dominio, un modelo como entidad.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/extract/ (un módulo nuevo y su registro en plan.py). Fuera: tipos de dominio nuevos. Si al hacerlo un caso no cabe en ningún tipo existente, se nombra como desconocido con su motivo, que es lo que el modelo ya prevé, y se anota en el inbox del desk; no se agrega un tipo dentro de esta tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer src/specir/extract/django_drf.py y facts.py como modelo: el extractor lee hechos, no código. Si a los hechos de sldb les falta algo para reconocer un comando de CLI (argparse o click), se pide por el inbox de sldb.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_extract_python_cli.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

specir extract sobre una copia del repo deskops deja en el store los comandos de su CLI, las funciones públicas que cada uno invoca y sus modelos, cada nodo con su capa, su origen observado y el archivo y la línea de donde salió. Las reglas sembradas de specIR corren sobre ese store sin error. Lo que no se pudo clasificar aparece como desconocido y contado.
