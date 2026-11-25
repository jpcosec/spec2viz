Task: task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir
Title: Sin marcador parity ni dependencia de spec2viz en las pruebas de IR
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-25T03:00:41Z'
  authority: generated
  via: save_document_payload
id: task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir
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

# Sin marcador parity ni dependencia de spec2viz en las pruebas de IR

## Rationale

_Explain why this task exists or the business driver behind it._

JP 2026-11-24: spec2viz continua como IR. Las pruebas de paridad ya comparan contra goldens versionados (tests/visual/goldens/spec2viz-2de1056*.json) y no necesitan spec2viz instalado; pero pyproject.toml todavia describe el marcador como 'compares specIR with spec2viz as the oracle; skipped when spec2viz is not installed', que ya no es cierto.

## Goal

_Describe the concrete result this task must produce._

La descripcion del marcador parity en pyproject.toml dice lo que hace hoy: compara specIR con los goldens congelados de spec2viz (revision 2de1056) en tests/visual/goldens/, sin necesitar spec2viz. Ninguna prueba se salta por falta de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Solo la linea del marcador en pyproject.toml ([tool.pytest.ini_options] markers). No se quita el marcador ni se tocan tests: los tests que importan o nombran spec2viz como dato (test_packaging.py comprueba que spec2viz no se instala; test_retirement_gate.py lo usa en fixtures del comprobador) se quedan.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo: /mnt/ssd/proyectos/SLDB_1/IR. 1) Reemplazar en pyproject.toml el texto del marcador por: 'parity: compares specIR with the frozen spec2viz outputs (revision 2de1056) in tests/visual/goldens/; spec2viz is not needed'. 2) Correr pytest -m parity -rs sobre tests/visual y confirmar 0 skipped.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -m parity -rs -p no:cacheprovider tests/visual

## Done When

_Name the observable condition that makes the task complete._

pyproject.toml describe parity con goldens y sin spec2viz; pytest -m parity -rs tests/visual pasa sin skipped.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-6735ed85d05b"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-6735ed85d05b`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-6735ed85d05b

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
