---
sldb:
  by: agent
  at: '2026-11-25T03:44:03Z'
  authority: generated
  via: create_document
id: task-las-pruebas-de-tests-test-mcp-extension-py-fallan-en-el-setup-el-server-mcp-cierra-la-conexion-al-ar
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las pruebas de tests/test_mcp_extension.py fallan en el setup: el server MCP cierra la conexion al arrancar sobre la copia del store

## Rationale

_Explain why this task exists or the business driver behind it._

Visto el 2026-11-25 al verificar specir mcp: tests/test_mcp_extension.py da 'MCPError: Connection closed' en session.initialize() del fixture mcp (served() de tests/conftest.py lanza python -m sldb mcp sobre la copia del store de la sesion con la extension de specIR). Ya fallaba en el commit anterior a specir mcp (564a82e~1), asi que no lo causo esa tarea. El mismo server sobre el store real de IR responde bien a initialize. Rompe la suite de IR y su integrate.

## Goal

_Describe the concrete result this task must produce._

Se identifica por que el server muere al arrancar sobre la copia del store de la sesion (fixtures store_copy y build_deskops_copy de tests/conftest.py) y se corrige la causa, de modo que tests/test_mcp_extension.py pase.

## Scope

_State what is in scope and what is out of scope._

tests/conftest.py (fixtures de copia y served) o el codigo de specIR que el server carga. Si la causa esta en sldb (sldb mcp o stores remove sobre la copia), parar y reportar con la reproduccion para pedirlo por inbox a sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir desde /mnt/ssd/proyectos/SLDB_1/IR: PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 python -m pytest -q -x tests/test_mcp_extension.py -k serves_its_tools. 2) Capturar el stderr del server: lanzar a mano el comando de served() sobre la copia que arma el fixture, o pasar errlog al cliente stdio en una prueba local, y leer el traceback. 3) Corregir la causa. 4) Correr tests/test_mcp_extension.py y tests/test_cli_mcp.py.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py tests/test_cli_mcp.py

## Done When

_Name the observable condition that makes the task complete._

Causa nombrada en el resumen con el traceback del server; tests/test_mcp_extension.py y tests/test_cli_mcp.py pasan.
