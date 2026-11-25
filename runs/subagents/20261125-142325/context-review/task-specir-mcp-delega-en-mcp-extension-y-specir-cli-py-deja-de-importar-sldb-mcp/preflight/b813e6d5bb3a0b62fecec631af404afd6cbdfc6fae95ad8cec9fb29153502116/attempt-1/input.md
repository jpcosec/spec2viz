FILE:desk/tasks/task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp.md
---
sldb:
  by: agent
  at: '2026-11-25T14:22:15Z'
  authority: generated
  via: create_document
id: task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp
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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-specir-mcp-delega-en-mcp-extension-y-specir-cli-py-deja-de-importar-sldb-mcp: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

