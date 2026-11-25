FILE:desk/tasks/task-las-pruebas-de-tests-test-mcp-extension-py-fallan-en-el-setup-el-server-mcp-cierra-la-conexion-al-ar.md
---
sldb:
  by: agent
  at: '2026-11-25T13:27:30Z'
  authority: generated
  via: save_document_payload
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

Causa confirmada por johanes (runs/coordinacion-johanes.md, 2026-11-25): served() en tests/conftest.py (l.~266) lanza 'python -m sldb mcp' con cwd=str(root) (la copia del store) y env={**os.environ}; la validacion exporta PYTHONPATH=src, relativo, que en el server apunta a <copia>/src; stderr: No module named 'specir'; el server muere antes de initialize (Connection closed). specIR no esta instalado en el venv compartido. Arreglo (una linea en tests/conftest.py, l.~269): env={**os.environ, 'PYTHONPATH': os.pathsep.join(p for p in (package_pythonpath(), os.environ.get('PYTHONPATH', '')) if p)}, con package_pythonpath de specir.install (absoluto). No instalar specIR en el venv. Con PYTHONPATH absoluto ya dio 14 passed en tests/test_mcp_extension.py y tests/test_cli_mcp.py.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py tests/test_cli_mcp.py

## Done When

_Name the observable condition that makes the task complete._

Causa nombrada en el resumen con el traceback del server; tests/test_mcp_extension.py y tests/test_cli_mcp.py pasan.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-las-pruebas-de-tests-test-mcp-extension-py-fallan-en-el-setup-el-server-mcp-cierra-la-conexion-al-ar: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

