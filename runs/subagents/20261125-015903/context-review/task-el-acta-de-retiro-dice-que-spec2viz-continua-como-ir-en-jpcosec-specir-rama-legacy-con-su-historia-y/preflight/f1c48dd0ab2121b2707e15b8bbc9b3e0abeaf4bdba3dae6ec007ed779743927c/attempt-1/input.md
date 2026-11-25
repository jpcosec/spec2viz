FILE:desk/tasks/task-el-acta-de-retiro-dice-que-spec2viz-continua-como-ir-en-jpcosec-specir-rama-legacy-con-su-historia-y.md
---
sldb:
  by: agent
  at: '2026-11-25T01:09:40Z'
  authority: generated
  via: create_document
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

1) Leer el acta y el gate. 2) Agregar la salvedad fechada 2026-11-24 y marcar el punto 9. 3) Nada de codigo.

## Validation

_List the checks required before this task can close._

- grep -n 'jpcosec/specir' docs/spec2viz/acta-de-retiro.md

## Done When

_Name the observable condition that makes the task complete._

El acta nombra jpcosec/specir, la rama legacy y la decision de JP del 2026-11-24, y el punto 9 esta marcado.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-acta-de-retiro-dice-que-spec2viz-continua-como-ir-en-jpcosec-specir-rama-legacy-con-su-historia-y: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

