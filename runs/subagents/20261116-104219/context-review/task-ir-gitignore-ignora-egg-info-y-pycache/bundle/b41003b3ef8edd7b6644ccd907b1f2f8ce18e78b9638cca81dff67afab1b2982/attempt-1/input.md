FILE:desk/tasks/task-ir-gitignore-ignora-egg-info-y-pycache.md
---
sldb:
  by: agent
  at: '2026-11-16T10:39:54Z'
  authority: generated
  via: save_document_payload
id: task-ir-gitignore-ignora-egg-info-y-pycache
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:pruebas
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-021128-suggestion-ir-gitignore-no-ignora-egg-info-ni-pycache-el-hook-de-scion-instala-ir-editable.md
depends_on: []
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- .gitignore
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR/.gitignore ignora *.egg-info/ y __pycache__/

## Rationale

_Explain why this task exists or the business driver behind it._

El hook pre-start de los ejecutores scion instala IR como editable (uv pip install -e IR[test]), lo que crea src/specir.egg-info/, y las pruebas dejan __pycache__/ en el árbol. IR/.gitignore solo ignora .sldb_cache/, .deskops.log y runs/subagents/*/session.jsonl, así que esos artefactos salen como no rastreados en cada git status y estorban al revisar el alcance de una tarea. sldb y deskops ya los ignoran. Origen: nota de scion desk/inbox/20261116-021128-suggestion-ir-gitignore-no-ignora-egg-info-ni-pycache-el-hook-de-scion-instala-ir-editable.md.

## Goal

_Describe the concrete result this task must produce._

git status de IR deja de listar src/specir.egg-info/ y los directorios __pycache__/.

## Scope

_State what is in scope and what is out of scope._

Dentro: agregar a IR/.gitignore dos líneas, *.egg-info/ y __pycache__/, al final y sin tocar las tres existentes. Fuera: borrar los artefactos del disco, cambiar otros archivos y cambiar el hook de scion.

## Implementation Path

_Outline the expected implementation route or affected surface._

Editar .gitignore en la raíz de IR agregando las dos líneas. No se borra nada del disco: los directorios quedan, solo dejan de aparecer como no rastreados. Comprobar que ningún archivo rastreado queda bajo esos patrones (git ls-files | grep -E 'egg-info/|__pycache__/' no encuentra nada), para que el cambio no oculte archivos que ya están en el repo. No hay código que probar, así que no se corre la suite.

## Validation

_List the checks required before this task can close._

- git diff .gitignore muestra solo dos líneas agregadas: *.egg-info/ y __pycache__/.
- git check-ignore -q src/specir.egg-info sale con rc 0, y git check-ignore -q tests/__pycache__ también (si ese directorio existe).
- git status --porcelain | grep -E 'egg-info|__pycache__' no encuentra nada.
- git ls-files | grep -E 'egg-info/|__pycache__/' no encuentra nada.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

.gitignore tiene las dos líneas nuevas, git status no lista egg-info ni __pycache__, y ningún archivo rastreado quedó ignorado.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:.gitignore
.sldb_cache/
.deskops.log
runs/subagents/*/session.jsonl

FILE:instruccion
Cold-bundle de la tarea task-ir-gitignore-ignora-egg-info-y-pycache: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- git diff .gitignore muestra solo dos líneas agregadas: *.egg-info/ y __pycache__/.
- git check-ignore -q src/specir.egg-info sale con rc 0, y git check-ignore -q tests/__pycache__ también (si ese directorio existe).
- git status --porcelain | grep -E 'egg-info|__pycache__' no encuentra nada.
- git ls-files | grep -E 'egg-info/|__pycache__/' no encuentra nada.
- deskops graph missing --root . sale con rc 0.

