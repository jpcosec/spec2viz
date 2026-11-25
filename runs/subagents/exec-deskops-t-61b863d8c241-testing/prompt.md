Task: task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac
Title: IR borra los goldens de spec2viz y las pruebas que los leen; la paridad se acredita por pruebas de aceptacion
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T14:54:37Z'
  authority: generated
  via: save_document_payload
id: task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac
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
---

# IR borra los goldens de spec2viz y las pruebas que los leen; la paridad se acredita por pruebas de aceptacion

## Rationale

_Explain why this task exists or the business driver behind it._

Decision de JP (2026-11-25, runs/coordinacion-johanes.md 11:50): 'Pitéate todos los goldens de spec2viz... tenemos que cumplir con features, no codigo. Mantenerlos solo genera ruido.' El guardrail pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas ya se reescribio en ese sentido.

## Goal

_Describe the concrete result this task must produce._

Que en IR no quede ningun golden de spec2viz ni prueba, helper o marcador que exista solo para compararse con ellos, y que la suite siga verde.

## Scope

_State what is in scope and what is out of scope._

tests/ y pyproject.toml de IR. Fuera: src/ (no se toca codigo de produccion), docs/spec2viz/ (la matriz y el acta quedan como historicos), el comando specir retirement check (queda sin prueba de gate).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR. 1) Inventario: grep -rln 'oracle\|goldens\|parity' tests/ y confirmar el conjunto contra esta lista (de una exploracion de johanes, no de correr la suite): BORRAR tests/visual/goldens/ (los JSON spec2viz-2de1056-*), tests/visual/oracle.py, parity.py, render_parity.py; tests/visual/test_render_parity.py, test_catalog_parity.py, test_visual_parity.py, test_notations_parity.py, test_sync_generation_parity.py; tests/test_matriz_cobertura_spec2viz.py y tests/visual/test_retirement_gate.py (leen el oraculo congelado); y dentro de test_render_cases.py, test_render_commands.py, test_schema.py, test_resources.py y test_lint_mermaid.py solo los casos *matches_spec2viz* y los que usan oracle.expect(...). Quitar el marcador parity de pyproject.toml (y cualquier -m parity en conftest o config). CONSERVAR las pruebas de comportamiento que no leen goldens: test_bpmn.py, test_cli.py, test_api.py, test_renderers.py (las de subcadena), test_catalog.py, test_catalog_annotations.py. Si el grep encuentra algo fuera de la lista, decidir con el mismo criterio (borra si solo existe para comparar con spec2viz) y anotarlo en result-summary.md. 2) Al final grep -rniE 'spec2viz-2de1056|oracle|goldens|parity' tests/ pyproject.toml no devuelve nada (salvo nombres de capacidades en docstrings, anotados). 3) Correr la suite completa de tests/visual y los archivos editados. Criterio (revision de johanes): se borra lo que compara con spec2viz, no lo que prueba una capacidad. Los casos de comportamiento dentro de archivos de paridad se MUEVEN a otro archivo antes de borrar el de paridad: al menos test_the_projected_states_of_the_blog_render de tests/visual/test_render_parity.py (proyeccion de la cadena del blog) va a tests/visual/test_render_projections.py o similar. Revisar tambien tests/conftest.py, test_refs_models.py y test_visual_names.py, que el grep marca. Antes de la suite, verificar que tests/extract y tests/models pasan (specIR ya esta instalado editable en el venv).

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider -n 4 tests/visual tests/test_cli_mcp.py

## Done When

_Name the observable condition that makes the task complete._

No queda tests/visual/goldens ni oracle/parity/render_parity, ni pruebas que comparen contra spec2viz, ni el marcador parity; el grep final esta vacio; la suite de tests/visual y los archivos editados pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-61b863d8c241"
