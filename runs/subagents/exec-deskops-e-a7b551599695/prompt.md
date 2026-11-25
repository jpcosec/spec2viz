Task: task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de
Title: specir extract describe una librería de Python con CLI con los tipos que ya tiene, y sobre el repo deskops deja sus comandos, operaciones y modelos como nodos con capa
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T19:27:17Z'
  authority: generated
  via: save_document_payload
id: task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de
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

# specir extract describe una librería de Python con CLI con los tipos que ya tiene, y sobre el repo deskops deja sus comandos, operaciones y modelos como nodos con capa

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): el qué y el dónde de un sistema son de specIR. Sus extractores cubren hoy una aplicación web (src/specir/extract/: django_drf, react_tsx, routes, sql), así que no describe a sldb, deskops ni a sí mismo. Nada lo impide: sldb ya entrega los hechos de código de Python (sldb/src/sldb/code/: py_module, py_calls, imports) y los tipos de specIR ya contemplan el caso, porque DomainOperationDoc se define como una capacidad "independent of how it is invoked (UI, CLI, job, agent)". Falta el extractor.

## Goal

_Describe the concrete result this task must produce._

Un extractor más, al lado de los que existen, que lee los hechos de Python de sldb y produce nodos de los tipos actuales: un comando de CLI como control y acción de interfaz, una función de la API pública como operación de API, lo que ejecuta como handler y operación de dominio, un modelo como entidad.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/extract/ (un módulo nuevo y su registro en plan.py). Fuera: tipos de dominio nuevos. Si al hacerlo un caso no cabe en ningún tipo existente, se nombra como desconocido con su motivo, que es lo que el modelo ya prevé, y se anota en el inbox del desk; no se agrega un tipo dentro de esta tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer src/specir/extract/django_drf.py y facts.py como modelo: el extractor lee hechos, no código. Si a los hechos de sldb les falta algo para reconocer un comando de CLI (argparse o click), se pide por el inbox de sldb.

Aclaraciones de la revisión: El cambio es en specIR (/mnt/ssd/proyectos/SLDB_1/IR, src/specir/extract/); deskops es solo el objetivo. Copia: un 'git worktree add --detach' de /mnt/ssd/proyectos/SLDB_1/deskops en origin/main bajo TMPDIR (o un clon local), quitado al final; el test usa un repo fixture chico en tests/fixtures/ con un comando argparse, una función pública, un handler y un modelo. Cobertura: argparse obligatorio (deskops lo usa); click solo si es trivial. API pública = nombres exportados por el paquete (__all__ o sin guion bajo en __init__); handler = la función que un subcomando de argparse llama (set_defaults(func=...) o equivalente); operación de dominio = lo que el handler llama dentro del paquete. Modelo = clase Pydantic o dataclass (los de deskops son modelos de sldb basados en Pydantic). Capa: según los tipos que ya tiene specIR (data/relation_types.yaml y las capas que use specir install); no se crean tipos. Reglas: specir lint (o el comando de reglas que tenga specIR; ver specir --help) sobre el store temporal, rc 0. Desconocido: nodo con motivo y una nota por 'deskops message send --to IR --kind unclear'; a sldb solo si falta un hecho de código, sin bloquear la tarea. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_extract_python_cli.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

specir extract sobre una copia del repo deskops deja en el store los comandos de su CLI, las funciones públicas que cada uno invoca y sus modelos, cada nodo con su capa, su origen observado y el archivo y la línea de donde salió. Las reglas sembradas de specIR corren sobre ese store sin error. Lo que no se pudo clasificar aparece como desconocido y contado.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-a7b551599695"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-a7b551599695`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-a7b551599695

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
