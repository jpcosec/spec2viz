FILE:desk/tasks/task-el-acta-de-retiro-dice-que-spec2viz-continua-como-ir-en-jpcosec-specir-rama-legacy-con-su-historia-y.md
---
sldb:
  by: agent
  at: '2026-11-25T02:27:36Z'
  authority: generated
  via: save_document_payload
id: task-el-acta-de-retiro-dice-que-spec2viz-continua-como-ir-en-jpcosec-specir-rama-legacy-con-su-historia-y
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

# El acta de retiro dice que spec2viz continua como IR en jpcosec/specir (rama legacy con su historia) y marca hecho el punto 9

## Rationale

_Explain why this task exists or the business driver behind it._

JP 2026-11-24: el remoto de IR es el repo de spec2viz. Se desarchivo jpcosec/spec2viz, se renombro a jpcosec/specir, master paso a legacy (historia de spec2viz intacta) y main es IR. El acta dice que el repo quedo archivado.

## Goal

_Describe the concrete result this task must produce._

docs/spec2viz/acta-de-retiro.md registra el cambio: spec2viz no queda archivado sino que continua como IR en jpcosec/specir (main = IR, legacy = historia de spec2viz); el punto 9 queda marcado como hecho con esta salvedad, con fecha y la decision de JP.

## Scope

_State what is in scope and what is out of scope._

Solo docs/spec2viz/acta-de-retiro.md (y gate-de-retiro.md si nombra el archivo).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo: /mnt/ssd/proyectos/SLDB_1/IR. Solo docs/spec2viz/acta-de-retiro.md (gate-de-retiro.md no se toca). Tres ediciones, sin borrar historia (se reemplaza el estado, se conserva lo que paso): 1) Punto 9 de la lista 'Lo que falta para declarar el retiro' (hoy empieza con '9. **Pendiente, último paso (coordinador, en GitHub).** Archivar spec2viz'): reemplazar ese item por '9. **Hecho el 2026-11-24, con cambio de JP.** El 2026-11-23 el coordinador archivó jpcosec/spec2viz; el 2026-11-24 JP decidió que spec2viz continúa como IR: el repo se desarchivó y se renombró a jpcosec/specir (las URL de spec2viz redirigen), la rama master pasó a llamarse legacy y conserva intacta la historia de spec2viz (con el store spec2viz/.sldb), y main es IR y la rama por defecto. spec2viz no queda archivado: legacy es su archivo.' 2) La frase de la cabecera que dice 'Lo único que queda es archivar el repo spec2viz en GitHub (punto 9 de «Lo que falta para declarar el retiro»), el último paso, que hace el coordinador; esta tarea no lo hace.' pasa a 'El punto 9 quedó hecho el 2026-11-24: spec2viz continúa como IR en jpcosec/specir, con su historia en la rama legacy.' 3) La linea 'Estado al 2026-11-23: el retiro está declarado; solo queda el punto 9.' pasa a 'Estado al 2026-11-24: el retiro está declarado y los nueve puntos están hechos.' Nada de codigo.

## Validation

_List the checks required before this task can close._

- grep -n "jpcosec/specir" docs/spec2viz/acta-de-retiro.md
- ! grep -n "Lo único que queda es archivar" docs/spec2viz/acta-de-retiro.md

## Done When

_Name the observable condition that makes the task complete._

El acta nombra jpcosec/specir y la rama legacy en el punto 9 marcado como hecho el 2026-11-24, la cabecera y la linea de estado ya no dicen que falta archivar.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-acta-de-retiro-dice-que-spec2viz-continua-como-ir-en-jpcosec-specir-rama-legacy-con-su-historia-y: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

