Task: task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo
Title: Cambios del momento del retiro de spec2viz: BPMN con exporter y targetNamespace de specir, clave de localStorage del catalogo de specir con migracion y goldens nuevos
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
  at: '2026-11-23T22:35:36Z'
  authority: generated
  via: save_document_payload
id: task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on:
- task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cambios del momento del retiro de spec2viz: BPMN con exporter y targetNamespace de specir, clave de localStorage del catalogo de specir con migracion y goldens nuevos

## Rationale

_Explain why this task exists or the business driver behind it._

Decision de JP del 2026-11-23 en task-jp-decide-declarar-el-retiro-de-spec2viz-sacar-spec2viz-sldb-del-universo-del-comprobador-y-archivar (recibo owner-1, punto 2): hacer ya los cambios del momento del retiro descritos en docs/spec2viz/acta-de-retiro.md, punto 8 (decision 3 del acta).

## Goal

_Describe the concrete result this task must produce._

El BPMN que emite specir lleva exporter='specir' y un targetNamespace de specir; la pagina del catalogo usa una clave de localStorage de specir y migra al cargar las anotaciones guardadas con spec2viz.catalog.annotations.v1 (sin perderlas y sin volver a escribir la clave vieja); los goldens afectados se regeneran con el comando del repo y quedan revisados en el diff.

## Scope

_State what is in scope and what is out of scope._

Emisor BPMN de specir, la pagina del catalogo (JS de localStorage) y sus goldens y tests en IR. Fuera: declarar el retiro en el acta y archivar el repo spec2viz (punto 3, lo hace el coordinador despues de attach_atom_edges en sldb); sacar spec2viz/.sldb del inventario y SV-A17 (punto 1, abierto).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ubicar con grep exporter=, targetNamespace y spec2viz.catalog.annotations.v1 en IR. 2) Cambiar el emisor BPMN y su test. 3) Clave nueva de localStorage con migracion desde la vieja y test (de JS o de la pagina generada). 4) Regenerar los goldens con el comando del repo y revisar el diff. 5) Marcar el punto 8 como hecho en el acta con fecha y commit.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los tests de BPMN, catalogo y goldens tocados

## Done When

_Name the observable condition that makes the task complete._

Los tests de BPMN y del catalogo pasan con los goldens nuevos; un test prueba la migracion de la clave vieja a la nueva; grep de spec2viz.catalog.annotations.v1 solo queda en la migracion; el acta registra el punto 8 hecho.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-97635c2c4cce"
