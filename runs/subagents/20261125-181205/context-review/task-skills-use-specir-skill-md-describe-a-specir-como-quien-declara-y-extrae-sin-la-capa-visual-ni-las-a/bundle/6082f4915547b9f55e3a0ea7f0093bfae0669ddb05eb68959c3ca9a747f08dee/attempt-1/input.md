FILE:desk/tasks/task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a.md
---
sldb:
  by: agent
  at: '2026-11-25T17:45:12Z'
  authority: generated
  via: create_document
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

## Validation

_List the checks required before this task can close._

- ! grep -nE 'the visual layer|same catalog page' skills/use-specir/SKILL.md

## Done When

_Name the observable condition that makes the task complete._

La skill no afirma que specIR dibuja ni que tiene interfaz; cada comando que nombra existe; lo decidido y sin ejecutar está marcado como tal con la fecha.

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

FILE:instruccion
Cold-bundle de la tarea task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- ! grep -nE 'the visual layer|same catalog page' skills/use-specir/SKILL.md

