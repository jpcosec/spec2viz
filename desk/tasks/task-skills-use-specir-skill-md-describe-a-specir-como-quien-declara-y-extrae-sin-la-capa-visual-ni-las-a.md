---
sldb:
  by: agent
  at: '2026-11-25T21:22:43Z'
  authority: generated
  via: save_document_payload
id: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- skills/use-specir/SKILL.md
- e0ae0115910bf7eb13f2cd9a30bd019cfbbb2deb
depends_on: []
pills: []
files:
- skills/use-specir/SKILL.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-la-skill-use-specir-describe-a-specir-como-quien-declara-y-extrae
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
