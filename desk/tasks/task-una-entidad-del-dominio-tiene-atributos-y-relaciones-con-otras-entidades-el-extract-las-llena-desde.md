---
sldb:
  by: agent
  at: '2026-11-25T22:52:42Z'
  authority: generated
  via: create_document
id: task-una-entidad-del-dominio-tiene-atributos-y-relaciones-con-otras-entidades-el-extract-las-llena-desde
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-el-modelo-de-specir-tiene-pantalla-y-navegacion-el-extract-las-llena-en-el-frontend-de-ejemplo-y-la
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# una entidad del dominio tiene atributos y relaciones con otras entidades, el extract las llena desde los modelos de Django y la notación ORCA las muestra

## Rationale

_Explain why this task exists or the business driver behind it._

Plan desk/drawer/plans/specir-plugin-de-sldb/ y decisión docs/decisiones/specir-es-un-plugin-de-sldb.md (JP, 2026-11-25). Nodo N5. JP: lo de ORCA va después de pantalla y navegación. DomainEntityDoc no dice qué atributos tiene una entidad ni cómo se relaciona con otra, y ORCA (objetos, relaciones, llamadas a la acción, atributos) no se puede declarar sin eso.

## Goal

_Describe the concrete result this task must produce._

Que specIR describa los objetos de un sistema con sus atributos, sus relaciones y lo que se puede hacer con ellos.

## Scope

_State what is in scope and what is out of scope._

Dentro: atributos de entidad y relación entre entidades con su cardinalidad en el modelo; su mapeo desde los hechos de modelos de Django; la notación ORCA como semilla. Fuera: leer código desde specIR, otros frameworks, y código por notación.

## Implementation Path

_Outline the expected implementation route or affected surface._

Proponer desde lo que debería ser. Revisar primero si TableDoc y la relación persisted_in ya cubren parte, para no duplicar. La llamada a la acción de ORCA se arma con lo que ya existe: las operaciones de dominio y las acciones de interfaz que actúan sobre la entidad.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/models/test_entity_attributes_and_relations.py tests/extract/test_blog_extraction.py
- python -m pytest -q tests/notations/test_orca_notation.py

## Done When

_Name the observable condition that makes the task complete._

Sobre tests/fixtures/blog_app, cada entidad sale con sus atributos y con sus relaciones a otras entidades, con cardinalidad. Una vista con la notación ORCA muestra objeto, atributos, relaciones y acciones, sin documentos sin glifo. Los datos nuevos llevan origen y verificación.
