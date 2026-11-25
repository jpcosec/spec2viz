Task: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a
Title: skills/use-specir/SKILL.md describe a specIR como quien declara y extrae, sin la capa visual ni las anotaciones del catálogo
Status: active
Current node: ritual-testing
Task type: task.docs
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T20:56:24Z'
  authority: generated
  via: save_document_payload
id: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-f73d09d73a37"
