---
sldb:
  by: agent
  at: '2026-11-25T05:27:45Z'
  authority: generated
  via: create_document
id: task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
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

Repo /mnt/ssd/proyectos/SLDB_1/IR. Formato del YAML: lista 'routes' de {method: GET|POST|PUT|PATCH|DELETE, route: '/api/...', title: opcional}. Funcion extract_routes(yaml_path, store) en src/specir/extract/routes.py: valida el YAML (method en mayusculas de la lista, route empieza con '/'; error legible si no), arma Planned('ApiOperationDoc', node_name('ApiOperationDoc', title o 'METHOD route'), {title, method, route}, 'declarado', ...) y escribe con write_plan como el resto (idempotente). Ver como django_drf.py:221 arma la ApiOperationDoc y como extract_frontend (__init__.py:56) las lee para invokes: solo toma las que tienen method, asi que quedan enlazables. Exportarla en specir.extract.__all__. Test nuevo tests/extract/test_declared_routes.py: (a) un YAML con dos rutas escribe dos ApiOperationDoc con origen declarado, method y route; (b) correrlo dos veces no duplica; (c) un method invalido da ValueError que nombra la entrada; (d) despues, extract_frontend sobre un TSX que llama fetch('/api/x', {method:'POST'}) con la ruta declarada enlaza invokes si los facts lo permiten, o el test deja constancia del no derivado esperado. Correr solo ese test y tests/extract/test_frontend_extraction.py.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/extract/test_declared_routes.py tests/extract/test_frontend_extraction.py

## Done When

_Name the observable condition that makes the task complete._

extract_routes escribe ApiOperationDoc declaradas idempotentes y tests/extract/test_declared_routes.py pasa con tests/extract/test_frontend_extraction.py.
