Task: task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr
Title: Las pruebas de IR encuentran el workspace de SLDB_1 por SPECIR_WORKSPACE y no por el directorio padre del repo
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T14:41:11Z'
  authority: generated
  via: save_document_payload
id: task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-55fcdf6eef4b"
