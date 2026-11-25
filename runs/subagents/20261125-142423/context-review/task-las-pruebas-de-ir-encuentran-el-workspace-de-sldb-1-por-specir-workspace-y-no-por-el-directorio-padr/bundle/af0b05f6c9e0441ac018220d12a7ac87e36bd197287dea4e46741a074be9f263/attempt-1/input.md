FILE:desk/tasks/task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr.md
---
sldb:
  by: agent
  at: '2026-11-25T14:22:22Z'
  authority: generated
  via: create_document
id: task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr
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

# Las pruebas de IR encuentran el workspace de SLDB_1 por SPECIR_WORKSPACE y no por el directorio padre del repo

## Rationale

_Explain why this task exists or the business driver behind it._

El integrate de IR (2026-11-25) corre la suite en una copia limpia en /mnt/ssd/tmp/sldb1/deskops-integrate-*/; tests/conftest.py:29 fija WORKSPACE = REPO.parent, y ahi no hay deskops: 18 errores 'the deskops store is missing'. desk/config.json ya exporta SPECIR_WORKSPACE=/mnt/ssd/proyectos/SLDB_1 en la suite del integrate.

## Goal

_Describe the concrete result this task must produce._

Que conftest.py tome el workspace de la variable SPECIR_WORKSPACE si existe y, si no, de REPO.parent como hoy.

## Scope

_State what is in scope and what is out of scope._

tests/conftest.py y un test chico. Fuera: el resto de fixtures.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR. tests/conftest.py:29: WORKSPACE = Path(os.environ['SPECIR_WORKSPACE']) if os.environ.get('SPECIR_WORKSPACE') else REPO.parent. Revisar que todo uso de WORKSPACE (l.~96 deskops, otros hermanos) pase por esa constante. Test nuevo tests/test_workspace_env.py que, con monkeypatch de la variable y reimportando o leyendo la funcion que la resuelve, compruebe ambos casos (extraer la resolucion a una funcion workspace_root() para poder probarla). No poner Task-Id en el commit de codigo: el closeout pone los trailers.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=$PWD/src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_workspace_env.py tests/test_mcp_extension.py

## Done When

_Name the observable condition that makes the task complete._

Con SPECIR_WORKSPACE apuntando a SLDB_1, los tests que usan el store de deskops encuentran el workspace desde una copia fuera de SLDB_1; tests/test_workspace_env.py pasa.

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
Cold-bundle de la tarea task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=$PWD/src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_workspace_env.py tests/test_mcp_extension.py

