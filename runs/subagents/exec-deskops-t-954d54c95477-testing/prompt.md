Task: task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp
Title: specir mcp delega en mcp_extension y specir/cli.py deja de importar sldb.mcp
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
  at: '2026-11-25T14:30:34Z'
  authority: generated
  via: save_document_payload
id: task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp
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

# specir mcp delega en mcp_extension y specir/cli.py deja de importar sldb.mcp

## Rationale

_Explain why this task exists or the business driver behind it._

El integrate de IR (2026-11-25) fallo en tests/test_imports.py: test_package_imports_only_the_public_sldb_api y test_only_the_extension_reaches_mcp, porque el comando specir mcp (ca00d20) importa sldb.mcp.server y sldb.mcp.mutability en src/specir/cli.py:66-67, y la regla del repo es que solo src/specir/mcp_extension.py alcanza sldb.mcp.

## Goal

_Describe the concrete result this task must produce._

Que solo mcp_extension.py importe sldb.mcp y que specir mcp siga funcionando igual.

## Scope

_State what is in scope and what is out of scope._

src/specir/cli.py, src/specir/mcp_extension.py y, si hace falta, tests/test_cli_mcp.py. Fuera: tests/test_imports.py (la regla no cambia).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR. Mover la llamada a sldb.mcp.server.serve(store, level=READ si None, actor, extensions=('specir.mcp_extension:register',)) a una funcion serve(store, level=None, actor=None) en src/specir/mcp_extension.py; cli.py:mcp importa specir.mcp_extension.serve (lazy, dentro del comando) y le pasa los argumentos. El help de --level no debe nombrar el modulo de sldb como import (texto libre esta bien). Tambien vale test_specir_has_no_mcp_server_of_its_own: no usar los nombres MCPServer, FastMCP, build_server ni .run("stdio") en src/specir.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=$PWD/src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py tests/test_cli_mcp.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_imports.py y tests/test_cli_mcp.py pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-954d54c95477"
