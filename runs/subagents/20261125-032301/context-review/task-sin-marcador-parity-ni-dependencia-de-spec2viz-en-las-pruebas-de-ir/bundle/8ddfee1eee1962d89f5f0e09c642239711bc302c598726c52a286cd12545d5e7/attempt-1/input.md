FILE:desk/tasks/task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir.md
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

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:instruccion
Cold-bundle de la tarea task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -m parity -rs -p no:cacheprovider tests/visual

