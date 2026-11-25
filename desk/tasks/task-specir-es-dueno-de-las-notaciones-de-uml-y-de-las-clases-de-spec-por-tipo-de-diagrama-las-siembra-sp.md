---
sldb:
  by: agent
  at: '2026-11-25T18:27:12Z'
  authority: generated
  via: save_document_payload
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

Aclaraciones de la revisión: Repo: /mnt/ssd/proyectos/SLDB_1/IR. Las ocho notaciones son los YAML de /mnt/ssd/proyectos/SLDB_1/sldb/src/sldb/notations/builtin/: activity, component-view-matrix, component, deployment, reflection, statechart, uml-class, uml-sequence; se mueven todas (BPMN y capas no están ahí y quedan fuera). Las clases de spec por tipo de diagrama son las que hoy importa specir.visual.spec_models desde sldb.notations; el mapeo tipo→clase se toma de ese módulo. Se siembran como specir/data/ igual que relation_types.yaml (el mismo camino de specir install). La exención a quitar es la de tests/test_imports.py que permite a specir.visual.spec_models importar sldb.notations (líneas 3-17 del docstring y su lista); quitarla y que el test pase. 'Las 38 specs validan' = un test que recorre los fixtures de specs de tests/visual (los que haya, contarlos) y los valida con las clases de specIR. sldb deja de exportarlas: eso es una nota al inbox de sldb, no un cambio en sldb. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_imports.py tests/test_install.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

En un store nuevo, specir install deja las notaciones registradas y sldb notations validate las acepta todas. Las 38 specs de tests/visual/fixtures validan contra las clases de specIR. Ningún módulo de specIR importa sldb.models.notation.diagram_specs ni lee sldb/notations/builtin, y la exención de tests/test_imports.py para esos dos módulos se quita.
