FILE:desk/tasks/task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac.md
---
sldb:
  by: agent
  at: '2026-11-25T14:23:49Z'
  authority: generated
  via: save_document_payload
id: task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac
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
Cold-bundle de la tarea task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider -n 4 tests/visual tests/test_cli_mcp.py

