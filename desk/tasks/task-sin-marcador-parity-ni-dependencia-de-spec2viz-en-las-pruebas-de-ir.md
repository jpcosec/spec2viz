---
sldb:
  by: agent
  at: '2026-11-25T01:08:48Z'
  authority: generated
  via: create_document
id: task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-goldens-de-la-capa-visual-capturados-de-spec2viz-una-sola-vez-y-las-pruebas-de-paridad-pasan-a-compa
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Sin marcador parity ni dependencia de spec2viz en las pruebas de IR

## Rationale

_Explain why this task exists or the business driver behind it._

Sigue a task-goldens-de-la-capa-visual-capturados-de-spec2viz-una-sola-vez-y-las-pruebas-de-paridad-pasan-a-compa: con los goldens en su lugar, el marcador parity y cualquier import o skip por spec2viz sobran.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml ya no declara el marcador parity, tests/conftest.py y tests/visual no importan ni nombran spec2viz como dependencia, y el script de captura queda borrado o documentado como historico.

## Scope

_State what is in scope and what is out of scope._

pyproject.toml, tests/conftest.py, tests/visual. Fuera: codigo de src/.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep -rn 'spec2viz\|parity' pyproject.toml tests. 2) Quitar marcador, skips e imports. 3) Correr solo tests/visual.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q tests/visual

## Done When

_Name the observable condition that makes the task complete._

grep -rn 'importorskip.*spec2viz\|mark.parity' tests pyproject.toml no devuelve nada y tests/visual pasa.
