FILE:desk/tasks/task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta.md
---
sldb:
  by: agent
  at: '2026-11-25T13:08:42Z'
  authority: generated
  via: create_document
id: task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-u1-esqueleto-de-la-ui-de-specir-en-ir-ui-con-tokens-de-papel-cascaron-de-pestanas-y-lentes-y-cliente
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
---

# U1b: el cascaron de la UI de specIR usa los tokens de papel y se parece a la maqueta

## Rationale

_Explain why this task exists or the business driver behind it._

Revision visual de johanes (2026-11-25 10:10, IR/runs/coordinacion-johanes.md) sobre U1 (1a9ec96): pasa tsc y vitest pero en Chrome no cumple el contrato de forma: botones nativos, explorador sin fondo piedra ni bordes, titulos en sans, sin rail inferior ni miga. paper-tokens.css esta copiado pero shell.css (9 lineas) no lo usa.

## Goal

_Describe the concrete result this task must produce._

Que el cascaron de IR/ui se vea como desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html#grafo: pestanas y lentes monoespaciadas con borde de 2 px y la activa en piedra; explorador con fondo piedra y borde; panel de documento con borde; titulos en serif (Newsreader); rail inferior; miga con el nombre del store en la cabecera.

## Scope

_State what is in scope and what is out of scope._

IR/ui/src (estilos del cascaron y los componentes del Shell) y su test. Fuera: contenido de las pestanas (U2-U9).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR, app IR/ui. Usar las variables --wb-* de src/styles/paper-tokens.css (copiado de sldb/surface; ver sldb/surface/DESIGN.md y como las aplica sldb/surface/src/styles/app.css, que se puede copiar en lo necesario citando origen) en vez de estilos propios; nada de colores escritos a mano. Botones de pestana y lente estilizados (sin apariencia nativa). Comparar abriendo en Chrome real la app (vite dev o build) y desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html#grafo lado a lado; guardar dos capturas en el run dir (app y maqueta) y citarlas en result-summary.md con las diferencias que queden. Ajustar src/Shell.test.tsx solo si cambian roles o nombres.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx

## Done When

_Name the observable condition that makes the task complete._

Las capturas de la app y de maqueta-ui.html#grafo en el run dir muestran el mismo cascaron (pestanas, lentes, columnas con fondo y bordes, titulos serif, rail, miga); shell.css usa los tokens --wb-*; tsc y vitest de src/Shell.test.tsx pasan.

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
Cold-bundle de la tarea task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx

