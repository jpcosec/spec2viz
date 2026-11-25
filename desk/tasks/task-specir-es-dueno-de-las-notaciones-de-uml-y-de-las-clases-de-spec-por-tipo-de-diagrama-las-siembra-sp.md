---
sldb:
  by: agent
  at: '2026-11-25T17:45:00Z'
  authority: generated
  via: create_document
id: task-specir-es-dueno-de-las-notaciones-de-uml-y-de-las-clases-de-spec-por-tipo-de-diagrama-las-siembra-sp
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

# specIR es dueño de las notaciones de UML y de las clases de spec por tipo de diagrama, las siembra specir.install y deja de importarlas de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

docs/decisiones/paridad-por-capacidades.md y el ADR de sldb mechanism-in-sldb-content-in-specir.md (JP, 2026-11-25): sldb conserva el mecanismo y specIR recibe el contenido. Hoy las ocho notaciones viven en sldb/src/sldb/notations/builtin/ y las clases de spec en sldb.models.notation.diagram_specs; specIR las importa desde dos módulos exentos de su regla de "solo API pública" (src/specir/visual/spec_models.py, notation_style.py).

## Goal

_Describe the concrete result this task must produce._

Que las notaciones de UML y las clases de spec por tipo de diagrama vivan en specIR, y que un store las reciba al instalar specIR en él.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/ (datos de notación, clases de spec, install.py, visual/spec_models.py, visual/notation_style.py) y tests/test_imports.py. Fuera: borrarlas de sldb (lo hace una tarea de sldb después de esta), la notación BPMN, la de capas.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer sldb/docs/architecture/notations-and-views.md y store-declaration.md. El mecanismo (NotationDoc, GlyphDoc, LinkDoc, resolver, validar) se sigue usando desde sldb.api; solo se muda el contenido.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_imports.py tests/test_install.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

En un store nuevo, specir install deja las notaciones registradas y sldb notations validate las acepta todas. Las 38 specs de tests/visual/fixtures validan contra las clases de specIR. Ningún módulo de specIR importa sldb.models.notation.diagram_specs ni lee sldb/notations/builtin, y la exención de tests/test_imports.py para esos dos módulos se quita.
