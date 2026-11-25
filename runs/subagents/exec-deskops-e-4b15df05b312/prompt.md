Task: task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
Title: Las operaciones de API de un backend que no es DRF salen de una tabla de rutas declarada en YAML
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
  at: '2026-11-25T05:58:18Z'
  authority: generated
  via: save_document_payload
id: task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
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

# Las operaciones de API de un backend que no es DRF salen de una tabla de rutas declarada en YAML

## Rationale

_Explain why this task exists or the business driver behind it._

T7 del plan graph_ui con D2 decidida por JP (tabla de rutas declarada): graph_ui no tiene tabla de rutas ni OpenAPI (if/elif en http.server), asi que extract no crea ApiOperationDoc y los invokes del frontend salen vacios. Plan desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md (medicion sobre graph_ui 36adfbb).

## Goal

_Describe the concrete result this task must produce._

Leer un YAML de rutas declaradas y escribir un ApiOperationDoc por entrada con origen 'declarado', para que extract_frontend pueda enlazar invokes.

## Scope

_State what is in scope and what is out of scope._

src/specir/extract (modulo nuevo routes.py y su entrada publica), el comando 'specir ux routes' si T2 ya trajo el grupo ux (si no, solo la funcion), y un test. Fuera: la regla de envoltorios HTTP (T6), el YAML real de graph_ui (vive en graph_ui).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR. Formato del YAML: lista 'routes' de {method: GET|POST|PUT|PATCH|DELETE, route: '/api/...', title: opcional}. Funcion extract_routes(yaml_path, store) en src/specir/extract/routes.py: valida el YAML (method en mayusculas de la lista, route empieza con '/'; error legible si no), arma Planned('ApiOperationDoc', node_name('ApiOperationDoc', title o 'METHOD route'), {title, method, route}, 'declarado', ...) y escribe con write_plan como el resto (idempotente). Ver como django_drf.py:221 arma la ApiOperationDoc y como extract_frontend (__init__.py:56) las lee para invokes: solo toma las que tienen method, asi que quedan enlazables. Exportarla en specir.extract.__all__. Test nuevo tests/extract/test_declared_routes.py: (a) un YAML con dos rutas escribe dos ApiOperationDoc con origen declarado, method y route; (b) correrlo dos veces no duplica; (c) un method invalido da ValueError que nombra la entrada; (d) despues, extract_frontend sobre un TSX que llama fetch('/api/x', {method:'POST'}) con la ruta declarada enlaza invokes si los facts lo permiten, o el test deja constancia del no derivado esperado. Correr solo ese test y tests/extract/test_frontend_extraction.py. Ajustes de la revision en frio (johanes), obligatorios: (1) el docstring de Planned.payload (plan.py:53) dice 'never inferido, never declarado'; esta tarea cambia ese contrato: Planned admite origen 'declarado' solo para entradas sin facts escritas por extract_routes, y el docstring y cualquier assert lo dicen asi; nada mas en write_plan cambia de comportamiento. (2) Choque de nombres: node_name('ApiOperationDoc', 'POST /api/save') coincide con el que deriva DRF (django_drf.py:221 usa f'{verb} {route}'); antes de escribir, si ya existe en el store una ApiOperationDoc con ese nombre y otro origen, extract_routes falla con ValueError legible que nombra la entrada y el origen existente, sin escribir nada; test (e). (3) Entradas borradas del YAML: las declaradas no tienen anclas y write_plan nunca las marca changed; extract_routes lista en su reporte (campo nuevo, p. ej. stale_declared) las ApiOperationDoc con origen declarado que ya no estan en la tabla, sin borrarlas; test (f).

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/extract/test_declared_routes.py tests/extract/test_frontend_extraction.py

## Done When

_Name the observable condition that makes the task complete._

extract_routes escribe ApiOperationDoc declaradas idempotentes, rechaza el choque con una derivada, reporta las declaradas que salieron de la tabla, el docstring de Planned.payload admite declarado, y tests/extract/test_declared_routes.py (a)-(f) pasa con tests/extract/test_frontend_extraction.py.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-4b15df05b312"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-4b15df05b312`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-4b15df05b312

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
