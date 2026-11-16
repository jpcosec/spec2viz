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
