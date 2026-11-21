---
sldb:
  by: agent
  at: '2026-11-21T09:34:18Z'
  authority: generated
  via: create_document
id: task-jp-decide-declarar-el-retiro-de-spec2viz-sacar-spec2viz-sldb-del-universo-del-comprobador-y-archivar
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
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP decide: declarar el retiro de spec2viz, sacar spec2viz/.sldb del universo del comprobador y archivar el repo spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: specir retirement check (con --path de deskops, UIs/graph_ui, pron, sldb y spec2viz/.sldb) da 0 dependencias en sldb, deskops, pron, graph_ui e IR. Quedan solo las 19 del store spec2viz/.sldb, que registra sus 7 modelos desde spec2viz.sldb_models, y la fila SV-A17, que depende de ese store. Lo último que se cerró: sldb gen_golden (cfa6477b), las filas de validate (3d0a436, closeout 9c343b9) y los oráculos de paridad congelados en goldens (c47111d, closeout 3bbc758). G5 opción A ya la decidió JP el 2026-11-16: el store se archiva con el repo, sin reapuntar los modelos. Los pasos que quedan son irreversibles o del momento del retiro: el acta, puntos 2 y 8.

## Goal

_Describe the concrete result this task must produce._

JP confirma (o cambia) tres cosas. 1) Sacar spec2viz/.sldb del inventario de la matriz (el universo del comprobador) y acreditar SV-A17 con G5, para que specir retirement check dé rc 0. 2) Hacer los cambios del momento del retiro (acta, punto 8): BPMN con exporter='specir' y targetNamespace de specir, clave de localStorage del catálogo de specir con migración de spec2viz.catalog.annotations.v1, y goldens nuevos. 3) Declarar el retiro en docs/spec2viz/acta-de-retiro.md y archivar el repo spec2viz (GitHub archive y su desk). Con la confirmación, 1 y 2 se despachan como tareas de IR (IR13), y 3 lo hace quien JP diga.

## Scope

_State what is in scope and what is out of scope._

Decisión de JP; nada se ejecuta antes.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- deskops review status --root .

## Done When

_Name the observable condition that makes the task complete._

JP registró su decisión (owner receipt) y las tareas resultantes quedaron creadas.
