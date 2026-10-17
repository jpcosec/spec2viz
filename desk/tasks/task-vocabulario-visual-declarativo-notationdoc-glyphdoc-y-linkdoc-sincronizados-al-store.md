---
id: task-vocabulario-visual-declarativo-notationdoc-glyphdoc-y-linkdoc-sincronizados-al-store
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-adr-spec2viz-es-dueño-del-vocabulario-visual-graph-ui-de-la-vista-generica-y-los-gestos.md
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Vocabulario visual declarativo: NotationDoc, GlyphDoc y LinkDoc sincronizados al store

## Rationale

_Explain why this task exists or the business driver behind it._

Para que los specs de spec2viz corran sobre graph_ui, la notacion tiene que ser datos en el store y no tablas en los renderers. Hoy MERMAID_RELATION, _SEQ_ARROW y el anidamiento por contains viven en codigo.

## Goal

_Describe the concrete result this task must produce._

spec2viz define NotationDoc/GlyphDoc/LinkDoc como modelos sldb, trae notaciones builtin en YAML (uml-class y statechart como pilotos), las valida y las escribe al store; SpecDoc referencia su notacion y SpecNodeDoc lleva el payload del elemento (atributos, metodos, guardas) para que la vista pueda dibujar compartimentos.

## Scope

_State what is in scope and what is out of scope._

IN: spec2viz/sldb_models.py (NotationDoc/GlyphDoc/LinkDoc, SpecDoc.notation+catalogo, SpecNodeDoc.data+collection), spec2viz/notation.py, una notacion builtin por tipo de diagrama en spec2viz/notations/ (uml-class, statechart, component, deployment, uml-sequence, activity, component-view-matrix, reflection), spec2viz/sldb_sync.py (NotationSync; extraccion de aristas para activity, matrix, reflection; aristas ordenadas; relaciones de mensaje por kind), spec2viz/notation_view.py (resolve_view, link comodin, orden), CLI notation list|validate|sync|view, diagram sync --notation, catalog sync, tests por tipo, README, CHANGELOG, docs/notation-contract.md. OUT: vista generica, gestos y edicion de vuelta (graph_ui); hacer que los renderers Mermaid/PlantUML lean la notacion.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Limpiar modelos huerfanos del store. 2) Modelos Pydantic en sldb_models.py con __references__ (SpecDoc.notation, NotationDoc.glyphs/links, GlyphDoc.notation, LinkDoc.notation/relation_type). 3) notation.py: NotationSpec (Pydantic) que lee un YAML con notation/glyphs/links, valida enums draw|line, ids unicos, relaciones del tipo de diagrama, where no vacio en glifos no-default. 4) sldb_sync.py: NotationSync.sync(name|path) escribe notation-<n>, glyph-<n>.<id>, link-<n>.<id> en <root>/sldb/notations/<n>/, crea RelationTypeDoc que falten; SpecSync.sync acepta notation y la sincroniza antes del spec. 5) CLI notation group + --notation en diagram sync. 6) Re-sync de los 7 specs del repo y verificacion sldb edges check.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/ -q
- spec2viz diagram sync docs/architecture/spec2viz/*.yml --strict
- sldb edges check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

tests en verde; 'spec2viz catalog sync --config docs/architecture/vistas.yml --store .sldb --strict' sincroniza los 9 specs con notacion; 'spec2viz notation view <id> --store .sldb' resuelve cada spec del catalogo sin skipped inesperados; sldb edges check OK; graph_ui /api/graph lista NotationDoc/GlyphDoc/LinkDoc y SpecDoc con category.
