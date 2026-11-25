Task: task-u1-esqueleto-de-la-ui-de-specir-en-ir-ui-con-tokens-de-papel-cascaron-de-pestanas-y-lentes-y-cliente
Title: U1: esqueleto de la UI de specIR en IR/ui con tokens de papel, cascaron de pestanas y lentes y cliente de sldb serve
Status: draft
Current node: ritual-execution
Task type: task.code
From drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-25T06:23:58Z'
  authority: generated
  via: save_document_payload
id: task-u1-esqueleto-de-la-ui-de-specir-en-ir-ui-con-tokens-de-papel-cascaron-de-pestanas-y-lentes-y-cliente
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-decision-de-jp-donde-vive-la-ui-nueva-de-specir-y-como-comparte-con-la-superficie-de-sldb
- task-decision-de-jp-en-que-se-escribe-la-ui-nueva-de-specir
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
---

# U1: esqueleto de la UI de specIR en IR/ui con tokens de papel, cascaron de pestanas y lentes y cliente de sldb serve

## Rationale

_Explain why this task exists or the business driver behind it._

Plan graph_ui de IR (desk/drawer/plans/graph-ui-diccionario-de-componentes), decisiones D7 y D10 de JP del 2026-11-25: UI nueva de specIR con paridad minima con la pagina de spec2viz (U1-U5).

## Goal

_Describe the concrete result this task must produce._

Una app Vite + React TSX en IR/ui que arranca, muestra el cascaron (explorador a la izquierda, pestanas Grafo, Anclajes y Composiciones, panel de documento a la derecha, lentes Lectura y Fierros) y habla con sldb serve.

## Scope

_State what is in scope and what is out of scope._

Solo IR/ui (nuevo): package.json, vite.config.ts, tsconfig, index.html, src/. Fuera: contenido de las pestanas (U2-U9).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR, app en IR/ui/. Contrato de forma: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md y la maqueta desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html (estructura del prototipo de Kimun, estetica del SLDB Workbench). Decisiones de JP: React con TSX (D10); la app COPIA de sldb/surface lo que necesita y no importa de @sldb/surface (D7), y cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit). Reglas: la UI no calcula, toda escritura es una operacion con nombre por sldb serve, sin datos inventados (si falta un dato se muestra que falta). No tocar sldb/. Tests de componentes con vitest y @testing-library/react; ningun control sin rol y nombre accesible (D3). Copiar de sldb (commit 39c51f6e de sldb origin/main o el HEAD que leas, citandolo): surface/src/core/client.ts (cliente de sldb serve) y surface/src/styles/paper-tokens.css (tokens --wb-*, ver surface/DESIGN.md). La base URL de sldb serve sale de VITE_SLDB_URL con default http://127.0.0.1:8765 (o el que use surface). Componente Shell con las tres pestanas (role tab) y las dos lentes; cada pestana muestra por ahora un vacio honesto ('sin contenido todavia'). Panel de documento vacio hasta que se elija un nodo. Test src/Shell.test.tsx: renderiza las tres pestanas por rol y nombre, cambiar de pestana cambia el panel, las lentes conmutan; el cliente copiado tiene un test minimo con fetch mockeado. Revision en frio de johanes (2026-11-25): la base URL NO es 8765: copiar el esquema de surface: VITE_SLDB_URL con default '/sldb' y proxy en vite.config.ts hacia SLDB_TARGET (default http://127.0.0.1:8085), ver surface/vite.config.ts:6, asi no hay CORS. client.ts y el lienzo importan tipos de surface/src/core/contract.ts: copiarlo tambien (con su cabecera de origen) o tsc falla.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx

## Done When

_Name the observable condition that makes the task complete._

npx tsc --noEmit y vitest de src/Shell.test.tsx pasan en IR/ui; los archivos copiados citan su origen.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-u1-esqueleto-de-la-ui-de-specir-en-ir-ui-con-tokens-de-papel-cascaron-de-pestanas-y-lentes-y-cliente"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-b3b53893f051"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-b3b53893f051`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-b3b53893f051

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
