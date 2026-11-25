---
sldb:
  by: agent
  at: '2026-11-25T03:37:46Z'
  authority: generated
  via: save_document_payload
id: task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- skills/use-specir/SKILL.md
- src/specir/cli.py
- tests/test_cli_mcp.py
- 564a82e3df55446accd998e28725410a814e611c
depends_on: []
pills: []
files:
- skills/use-specir/SKILL.md
- src/specir/cli.py
- tests/test_cli_mcp.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
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

Repo: /mnt/ssd/proyectos/SLDB_1/IR (src/ y tests/ cuelgan de ahi). 1) En src/specir/cli.py, un comando click 'mcp' montado en main: opciones --store (ruta, requerida), --level (int, default sldb.mcp.mutability.READ) y --actor (str, default None); llama sldb.mcp.server.serve(store, level=level, actor=actor, extensions=('specir.mcp_extension:register',)). Docstring de una linea para --help: 'Serve sldb's MCP server on a store with specIR's tools (specir_types, specir_nodes, specir_rules, specir_impact) already loaded.' 2) Test NUEVO tests/test_cli_mcp.py, siguiendo como tests/test_mcp_extension.py arma un store y llama sldb.mcp.server.build_server(store, extensions=[sldb.mcp.extension.load_extension('specir.mcp_extension:register')]): (a) el server tiene las cuatro tools specir_*; (b) con click.testing.CliRunner, 'specir mcp --help' sale 0 y nombra --store; (c) monkeypatch de sldb.mcp.server.serve para capturar argumentos: 'specir mcp --store X' llega con extensions=('specir.mcp_extension:register',) y level READ. Sin levantar stdio. 3) En skills/use-specir/SKILL.md, agregar la linea: '- MCP: specir mcp --store <store del proyecto> levanta el server MCP de sldb con las tools de specIR cargadas (igual que sldb mcp --extension specir.mcp_extension:register).' Correr solo tests/test_cli_mcp.py y tests/test_mcp_extension.py.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cli_mcp.py tests/test_mcp_extension.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_cli_mcp.py (nuevo) cubre (a) las cuatro tools, (b) --help y (c) los argumentos que llegan a serve; pasa junto con tests/test_mcp_extension.py.
