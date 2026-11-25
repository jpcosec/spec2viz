Task: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a
Title: skills/use-specir/SKILL.md describe a specIR como quien declara y extrae, sin la capa visual ni las anotaciones del catálogo
Status: draft
Current node: ritual-execution
Task type: task.docs
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-docs] TaskDocsDoc:task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a: Una tarea task.docs se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:29:04Z'
  authority: generated
  via: save_document_payload
id: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# skills/use-specir/SKILL.md describe a specIR como quien declara y extrae, sin la capa visual ni las anotaciones del catálogo

## Rationale

_Explain why this task exists or the business driver behind it._

docs/decisiones/paridad-por-capacidades.md (JP, 2026-11-25). La skill abre diciendo que specIR es "the visual layer" con "same renderers, same catalog page", y dedica una sección a las anotaciones del catálogo por sldb serve, que se retiran. Un agente que la lea va a construir sobre lo que ya no es.

## Goal

_Describe the concrete result this task must produce._

Que la skill diga qué hace specIR hoy y a dónde se va para ver o editar un diagrama.

## Scope

_State what is in scope and what is out of scope._

Dentro: skills/use-specir/SKILL.md y sus referencias. Fuera: el código, la skill deskops-workflow (ya corregida).

## Implementation Path

_Outline the expected implementation route or affected surface._

Comprobar cada comando que la skill nombre corriendo su --help; no describir como hecho lo que solo está decidido.

Aclaraciones de la revisión: Repo: /mnt/ssd/proyectos/SLDB_1/IR. Dentro: skills/use-specir/SKILL.md y los archivos que ese SKILL.md enlaza dentro de skills/use-specir/. Leer docs/decisiones/paridad-por-capacidades.md. Para ver o editar un diagrama se va a la vista de notación de graph_ui (UIs/graph_ui, vista specs/notation); specIR declara y extrae. Lo decidido sin ejecutar se marca con '(decidido 2026-11-25, sin ejecutar)' en la línea. 'El comando existe' = su --help sale con rc 0. La validación con '!' es negación de shell (el grep no debe encontrar nada).

## Validation

_List the checks required before this task can close._

- ! grep -nE 'the visual layer|same catalog page' skills/use-specir/SKILL.md

## Done When

_Name the observable condition that makes the task complete._

La skill no afirma que specIR dibuja ni que tiene interfaz; cada comando que nombra existe; lo decidido y sin ejecutar está marcado como tal con la fecha.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-3a1e7ef9d105"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-3a1e7ef9d105`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-3a1e7ef9d105

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
