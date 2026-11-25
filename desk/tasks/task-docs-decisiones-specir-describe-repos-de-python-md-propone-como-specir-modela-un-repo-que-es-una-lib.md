---
sldb:
  by: agent
  at: '2026-11-25T19:12:45Z'
  authority: generated
  via: create_document
id: task-docs-decisiones-specir-describe-repos-de-python-md-propone-como-specir-modela-un-repo-que-es-una-lib
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs/decisiones/specir-describe-repos-de-python.md propone cómo specIR modela un repo que es una librería de Python con CLI, con alternativas y recomendación para JP

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): el qué y el dónde de un sistema son de specIR, que los extrae del código, y los átomos que hoy describen qué es o cómo funciona algo estarían en el lugar equivocado. Pero los extractores de specIR cubren una aplicación web (src/specir/extract/: django_drf, react_tsx, routes, sql) y sus tipos de dominio van del control de interfaz a la tabla. sldb, deskops y specIR mismo son librerías de Python con CLI: hoy specIR no los puede describir, así que no puede reemplazar a esos átomos ni servir de dónde para sus decisiones.

## Goal

_Describe the concrete result this task must produce._

Un documento de decisión, en el formato de docs/decisiones/, que diga qué nodos y qué capas tendría un repo de Python con CLI, de dónde salen, y qué se reutiliza.

## Scope

_State what is in scope and what is out of scope._

Dentro: el documento, con una prueba de concepto de lectura sobre el repo deskops. Fuera: implementar el extractor (tarea posterior, tras la elección de JP), tocar los tipos de dominio.

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de proponer tipos nuevos, leer qué entrega ya sldb sobre código Python: sldb.api.code (code_facts), los documentos de símbolo de sldb selfdoc (sldb/knowledge/symbols/) y las anclas de código. Decir por cada nodo propuesto si es un tipo que specIR ya tiene, un documento que sldb ya produce, o algo nuevo y por qué.

## Validation

_List the checks required before this task can close._

- test -f docs/decisiones/specir-describe-repos-de-python.md

## Done When

_Name the observable condition that makes the task complete._

El documento responde: qué capas tiene un repo así, qué tipo de nodo va en cada una, de qué hechos de código sale cada nodo, qué queda sin poder extraerse y se nombra como desconocido, y cuánto de lo que hoy dicen los átomos de qué, cómo y dónde de deskops quedaría cubierto, medido sobre una muestra. Trae al menos dos alternativas y una recomendación, y queda marcado como pendiente de la elección de JP.
