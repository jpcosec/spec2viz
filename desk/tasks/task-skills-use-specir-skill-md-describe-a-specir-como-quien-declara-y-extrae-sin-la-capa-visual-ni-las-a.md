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
