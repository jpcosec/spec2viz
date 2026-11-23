Task: task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita
Title: specir retirement check da rc 0: spec2viz/.sldb sale del inventario de la matriz y SV-A17 se acredita con G5 opcion A
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
  at: '2026-11-23T18:12:27Z'
  authority: generated
  via: save_document_payload
id: task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
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

# specir retirement check da rc 0: spec2viz/.sldb sale del inventario de la matriz y SV-A17 se acredita con G5 opcion A

## Rationale

_Explain why this task exists or the business driver behind it._

Decision de JP del 2026-11-23 en task-jp-decide-declarar-el-retiro-de-spec2viz-sacar-spec2viz-sldb-del-universo-del-comprobador-y-archivar (recibo owner-2, punto 1, 'dale' tras recibir el contexto): sacar spec2viz/.sldb del inventario de la matriz (el universo del comprobador) y acreditar SV-A17 citando G5 (opcion A, decidida el 16-nov: spec2viz/.sldb se archiva con el repo spec2viz), para que specir retirement check de rc 0. Hoy quedan solo las 19 dependencias de ese store y la fila SV-A17.

## Goal

_Describe the concrete result this task must produce._

specir retirement check (con los --path de deskops, UIs/graph_ui, pron, sldb y el resto del universo, sin spec2viz/.sldb) sale con rc 0; docs/spec2viz/matriz-de-cobertura.md acredita SV-A17 citando G5 opcion A (16-nov) y el acta registra el punto 2 hecho con fecha y commit.

## Scope

_State what is in scope and what is out of scope._

La declaracion del inventario o universo del comprobador en IR (donde specir retirement check toma sus --path), matriz-de-cobertura.md (fila SV-A17), acta-de-retiro.md (G5 y punto 2) y los tests del comprobador. Fuera: los cambios del momento del retiro (tarea task-cambios-del-momento-del-retiro-de-spec2viz-bpmn-con-exporter-y-targetnamespace-de-specir-clave-de-lo, va despues) y declarar el retiro y archivar spec2viz (punto 3, coordinador).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ubicar como se arma el universo del comprobador (config o argumentos) y correr specir retirement check para tener la linea base (19 dependencias de spec2viz/.sldb y SV-A17). 2) Sacar spec2viz/.sldb del inventario. 3) Acreditar SV-A17 con la cita de G5 opcion A. 4) Correr el comprobador: rc 0. 5) Actualizar el acta.

## Validation

_List the checks required before this task can close._

- specir retirement check con el universo declarado; TMPDIR=/dev/shm pytest -q de los tests del comprobador

## Done When

_Name the observable condition that makes the task complete._

specir retirement check sale con rc 0 y su salida queda en el informe junto a la linea base; los tests del comprobador pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-70136817bdf9"
