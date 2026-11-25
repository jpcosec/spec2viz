Task: task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom
Title: Declarar el retiro de spec2viz en el acta: comprobador en rc 0, catalog build medido y cambios del momento del retiro hechos
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.docs
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-docs] TaskDocsDoc:task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom: Una tarea task.docs se cierra con recibos evidence aceptados e intactos de commit y document (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "commit" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom-bundle-1 {"kind":"bundle"})

---
sldb:
  by: agent
  at: '2026-11-24T00:37:49Z'
  authority: generated
  via: save_document_payload
id: task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Declarar el retiro de spec2viz en el acta: comprobador en rc 0, catalog build medido y cambios del momento del retiro hechos

## Rationale

_Explain why this task exists or the business driver behind it._

Decision de JP del 2026-11-23 en task-jp-decide-declarar-el-retiro-de-spec2viz-sacar-spec2viz-sldb-del-universo-del-comprobador-y-archivar (recibos owner-1 y owner-2, punto 3): declarar el retiro cuando sldb cerrara attach_atom_edges y specir catalog build terminara en un tiempo razonable. Ambas condiciones se cumplen: sldb cerro task-matching-attach-atom-edges-... (c377aff6) y el coordinador midio el 2026-11-23 specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml en 55,8 s con rc 0 y 1,7 GB de RSS (antes no terminaba en 300 s); specir retirement check da rc 0 (punto 1, e6e369d) y los cambios del momento del retiro estan hechos (punto 2, 109684f).

## Goal

_Describe the concrete result this task must produce._

docs/spec2viz/acta-de-retiro.md declara el retiro con fecha 2026-11-23: el estado de cabecera pasa de 'no declarado' a 'declarado'; la seccion de medicion de catalog build trae la medicion nueva; la salida del comprobador muestra rc 0; los items de 'Lo que falta para declarar el retiro' quedan marcados hechos con su commit; el punto 9 (archivar el repo spec2viz) queda como el ultimo paso, que hace el coordinador en GitHub; el acta registra que los oraculos de paridad (punto 6) se retiran al declarar, o el motivo si no.

## Scope

_State what is in scope and what is out of scope._

Solo docs/spec2viz/acta-de-retiro.md y, si hace falta, matriz-de-cobertura.md. Fuera: codigo y el archivo del repo en GitHub.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr specir retirement check con el universo declarado y guardar su salida. 2) Actualizar cabecera, medicion, salida del comprobador y la lista de pendientes con fechas y commits. 3) Revisar que el acta no se contradiga (buscar 'no declarado').

## Validation

_List the checks required before this task can close._

- specir retirement check rc 0; grep -n 'no declarado' docs/spec2viz/acta-de-retiro.md solo en historia fechada

## Done When

_Name the observable condition that makes the task complete._

El acta dice retiro declarado el 2026-11-23, sin frases que lo contradigan, con la medicion de catalog build y la salida rc 0 del comprobador.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-declarar-el-retiro-de-spec2viz-en-el-acta-comprobador-en-rc-0-catalog-build-medido-y-cambios-del-mom"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-ca0f0e14eaaa-a2"
