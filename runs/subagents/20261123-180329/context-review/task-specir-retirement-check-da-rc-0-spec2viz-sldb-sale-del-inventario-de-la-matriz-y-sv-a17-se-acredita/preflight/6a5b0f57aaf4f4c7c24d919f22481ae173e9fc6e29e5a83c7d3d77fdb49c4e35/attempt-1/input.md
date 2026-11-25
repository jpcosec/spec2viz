FILE:desk/tasks/task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita.md
---
sldb:
  by: agent
  at: '2026-11-23T18:03:08Z'
  authority: generated
  via: create_document
id: task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

