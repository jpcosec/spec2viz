Task: task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca
Title: specir mcp: el punto de entrada propio de specIR levanta el server MCP de sldb con su extension ya cargada
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "bundle") (seen: {}) (witness: ReviewDoc:review-task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca-preflight-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T02:28:18Z'
  authority: generated
  via: save_document_payload
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

Repo: /mnt/ssd/proyectos/SLDB_1/IR (src/ y tests/ cuelgan de ahi). 1) En src/specir/cli.py, un comando click 'mcp' montado en main: opciones --store (ruta, requerida), --level (int, default sldb.mcp.mutability.READ) y --actor (str, default None); llama sldb.mcp.server.serve(store, level=level, actor=actor, extensions=('specir.mcp_extension:register',)). Docstring de una linea para --help: 'Serve sldb's MCP server on a store with specIR's tools (specir_types, specir_nodes, specir_rules, specir_impact) already loaded.' 2) Test NUEVO tests/test_cli_mcp.py, siguiendo como tests/test_mcp_extension.py arma un store y llama sldb.mcp.server.build_server(store, extensions=[sldb.mcp.extension.load_extension('specir.mcp_extension:register')]): (a) el server tiene las cuatro tools specir_*; (b) con click.testing.CliRunner, 'specir mcp --help' sale 0 y nombra --store; (c) monkeypatch de sldb.mcp.server.serve para capturar argumentos: 'specir mcp --store X' llega con extensions=('specir.mcp_extension:register',) y level READ. Sin levantar stdio. 3) En skills/use-specir/SKILL.md, agregar la linea: '- MCP: specir mcp --store <store del proyecto> levanta el server MCP de sldb con las tools de specIR cargadas (igual que sldb mcp --extension specir.mcp_extension:register).' Correr solo tests/test_cli_mcp.py y tests/test_mcp_extension.py.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cli_mcp.py tests/test_mcp_extension.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_cli_mcp.py (nuevo) cubre (a) las cuatro tools, (b) --help y (c) los argumentos que llegan a serve; pasa junto con tests/test_mcp_extension.py.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-specir-mcp-el-punto-de-entrada-propio-de-specir-levanta-el-server-mcp-de-sldb-con-su-extension-ya-ca"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-3d0893847263"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-3d0893847263`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-3d0893847263

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
