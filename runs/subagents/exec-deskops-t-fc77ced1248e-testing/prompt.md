Task: task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash
Title: Los nombres de relacion de specIR quedan acotados a 255 bytes con un resumen con hash
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
From drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash-bundle-1 {"kind":"bundle"})

---
sldb:
  by: agent
  at: '2026-11-25T06:10:18Z'
  authority: generated
  via: save_document_payload
id: task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash
status: ready_for_testing
summary: ''
tags: []
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-fc77ced1248e"
