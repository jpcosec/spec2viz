Task: task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta
Title: U1b: el cascaron de la UI de specIR usa los tokens de papel y se parece a la maqueta
Status: active
Current node: ritual-testing
Task type: task.code
From drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T13:37:22Z'
  authority: generated
  via: save_document_payload
id: task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-u1b-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-f68fc4d93dac"
