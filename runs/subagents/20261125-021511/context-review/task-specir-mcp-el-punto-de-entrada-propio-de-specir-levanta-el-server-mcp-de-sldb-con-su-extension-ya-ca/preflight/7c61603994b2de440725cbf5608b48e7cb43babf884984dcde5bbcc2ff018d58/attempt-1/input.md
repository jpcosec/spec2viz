FILE:desk/tasks/task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca.md
---
sldb:
  by: agent
  at: '2026-11-25T01:09:20Z'
  authority: generated
  via: create_document
id: task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca
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

# specir mcp: el punto de entrada propio de specIR levanta el server MCP de sldb con su extension ya cargada

## Rationale

_Explain why this task exists or the business driver behind it._

JP 2026-11-24 lo pidio: hoy specIR se arranca con 'sldb mcp --store <store> --extension specir.mcp_extension:register', y desde fuera specIR no tiene MCP propio. Se mantiene el mecanismo de extension (no se duplica server, guarda, propuestas ni undo de sldb). Es la excepcion aprobada a la regla de src/specir/cli.py de no envolver comandos de sldb.

## Goal

_Describe the concrete result this task must produce._

'specir mcp --store <ruta> [--level N] [--actor A]' arranca sldb.mcp.server.serve con specir.mcp_extension:register cargada; 'specir mcp --help' lo explica; las tools specir_* aparecen.

## Scope

_State what is in scope and what is out of scope._

src/specir/cli.py (comando mcp), su test y skills/use-specir/SKILL.md (una linea). Fuera: cambios en sldb y en mcp_extension.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer sldb.mcp.server.serve (firma: store, level, actor, extensions). 2) Comando click 'mcp' que llama serve con extensions=('specir.mcp_extension:register',). 3) Test: build_server con la extension registra specir_types/specir_nodes/specir_rules/specir_impact (sin levantar stdio). 4) Correr solo ese test.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q tests/test_cli_mcp.py

## Done When

_Name the observable condition that makes the task complete._

specir mcp --help existe y el test que construye el server por ese camino ve las cuatro tools specir_*; pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

