---
id: task-auditoria-de-empaquetado-version-rango-de-sldb-metadata-editable-mmdc-import-de-structurednldoc
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references: []
depends_on: []
pills: []
files: []
task_type: closeout
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Auditoria de empaquetado: version, rango de sldb, metadata editable, mmdc, import de StructuredNLDoc

## Rationale

_Explain why this task exists or the business driver behind it._

El coordinador audito el bundle (2026-10-18): pyproject dice 0.1.0 y el CHANGELOG ya registra 0.2.0; el rango de structuredLanguageDB difiere entre pyproject y CHANGELOG; la METADATA instalada esta vieja; mmdc no esta documentado como dependencia externa; sldb_models importa de sldb.models.structured_doc en vez de la superficie publica sldb.api.

## Goal

_Describe the concrete result this task must produce._

pyproject y CHANGELOG alineados (version 0.2.0, structuredLanguageDB>=0.1.10), instalacion editable refrescada, mmdc documentado en el README como dependencia externa opcional, y el import de StructuredNLDoc via sldb.api en cuanto sldb lo exponga (pedido a sldb-04).

## Scope

_State what is in scope and what is out of scope._

IN: pyproject.toml, CHANGELOG.md, README.md (Install), spec2viz/sldb_models.py (import). OUT: publicar release; cambios en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python -m pytest tests/ -q
- grep -n 'version\|structuredLanguageDB' pyproject.toml CHANGELOG.md

## Done When

_Name the observable condition that makes the task complete._

grep de version y rango coherentes; pip show structuredLanguageDB/spec2viz con la metadata nueva; README menciona mmdc; tests verdes; commit atomico pusheado.
