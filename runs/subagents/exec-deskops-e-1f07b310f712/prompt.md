Task: task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash
Title: Los nombres de relacion de specIR quedan acotados a 255 bytes con un resumen con hash
Status: active
Current node: ritual-testing
Task type: task.code
From drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T05:58:10Z'
  authority: generated
  via: save_document_payload
id: task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash
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
from_drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
---

# Los nombres de relacion de specIR quedan acotados a 255 bytes con un resumen con hash

## Rationale

_Explain why this task exists or the business driver behind it._

T1 del plan graph_ui: extract_frontend sobre graph_ui aborta con OSError Errno 36 File name too long; 21 de 133 relaciones pasan de 250 bytes (max 266). Plan desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md (medicion sobre graph_ui 36adfbb).

## Goal

_Describe the concrete result this task must produce._

Que edge_name nunca produzca un nombre de mas de 255 bytes, de forma determinista y estable.

## Scope

_State what is in scope and what is out of scope._

Solo src/specir/extract/plan.py (edge_name) y un test. Fuera: nombres de nodos, otros extractores, migracion de stores existentes.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR. edge_name (src/specir/extract/plan.py:65) concatena prefijo, slug del origen, relacion y slug del destino, y los nombres ya llevan la ruta completa del componente. Contrato: si el nombre completo cabe en 200 bytes UTF-8 queda igual (los stores existentes no cambian); si no, se recorta a un prefijo legible y se termina con '-' + los 12 primeros hex del sha256 del nombre completo, total <= 200 bytes (margen para el sufijo .yaml del archivo). Determinista: la misma entrada da el mismo nombre; dos entradas distintas largas dan nombres distintos. Test nuevo tests/extract/test_edge_name_bounded.py: (a) nombre corto sin cambios; (b) un origen con ruta profunda (> 300 bytes) da un nombre <= 200 bytes que termina en el hash; (c) dos destinos largos que solo difieren al final dan nombres distintos; (d) extract_frontend sobre un arbol temporal con un componente TSX en una ruta profunda escribe sin OSError (si el fixture TSX necesita tree-sitter-typescript, ya esta en el venv). Correr solo ese test y tests/extract/test_frontend_extraction.py. Agregados de la revision en frio (johanes): Planned.path (plan.py:49) tambien usa el nombre (DOCUMENT_DIR/<name>.md), asi que el test comprueba ademas len(Path(p.path).name.encode()) <= 255 para el .md y el .yaml del shard; y (e) el recorte corta en un limite de byte UTF-8 valido: probar edge_name con un nombre largo con caracteres multibyte (llamando al recorte directamente si slug los quitaria) y que el resultado decodifique como UTF-8.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/extract/test_edge_name_bounded.py tests/extract/test_frontend_extraction.py

## Done When

_Name the observable condition that makes the task complete._

tests/extract/test_edge_name_bounded.py cubre (a)-(e), incluido el largo del nombre de archivo de Planned.path, y pasa junto con tests/extract/test_frontend_extraction.py.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-1f07b310f712"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-1f07b310f712`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-1f07b310f712

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
