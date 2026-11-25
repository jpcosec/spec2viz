---
sldb:
  by: agent
  at: '2026-11-25T22:50:19Z'
  authority: generated
  via: create_document
id: task-los-exportes-de-texto-leen-la-vista-que-resuelve-sldb-y-se-borra-la-representacion-paralela-de-speci
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
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# los exportes de texto leen la vista que resuelve sldb, y se borra la representación paralela de specir.visual

## Rationale

_Explain why this task exists or the business driver behind it._

Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo R2. Comprobado el 2026-11-25: los exportes de PlantUML, Mermaid, D2, Vega y BPMN XML importan todos de specir.visual.ir (SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, ClassIR, MatrixIR). Esa representación, con projections.py, normalize.py, compilers/, schema.py, spec_models.py y notation_style.py, suma 1.072 líneas y repite lo que sldb ya resuelve como vista.

## Goal

_Describe the concrete result this task must produce._

Que haya una sola representación de un diagrama, la vista resuelta de sldb, y que los exportes de texto partan de ella.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/visual/renderers/ (los exportes de texto), los módulos de la representación paralela y sus pruebas. Fuera: los renderers de HTML y la página del catálogo (tienen su propio retiro), y la API de sldb: si la vista resuelta no trae algo que un exporte necesita, se pide por el inbox de sldb y ese exporte queda pendiente y declarado.

## Implementation Path

_Outline the expected implementation route or affected surface._

Primero medir: por cada exporte, qué campos de su IR usa y si la vista resuelta los trae. Con esa tabla se decide el orden; se migra un exporte por vez, con su prueba de aceptación sobre lo que hace (el texto es válido y nombra los nodos y relaciones del diagrama), no sobre una salida idéntica. Solo se usa la API pública de sldb.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/visual
- ! grep -rn 'specir.visual.ir' src/specir/visual/renderers

## Done When

_Name the observable condition that makes the task complete._

Cada exporte de texto recibe la vista resuelta por sldb y produce su salida para los tipos de diagrama que cubría antes. No existen src/specir/visual/ir.py, projections.py, normalize.py, compilers/, schema.py, spec_models.py ni notation_style.py, o los que quedan están listados con el motivo y el pedido a sldb que los sostiene. La suite pasa.
