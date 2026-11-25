---
sldb:
  by: agent
  at: '2026-11-25T06:07:47Z'
  authority: generated
  via: create_document
id: task-u9-anclajes-muestra-la-fuente-con-lineas-y-el-fragmento-resaltado-el-selector-su-estado-y-los-nodos
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

# U9: Anclajes muestra la fuente con lineas y el fragmento resaltado, el selector, su estado y los nodos que se apoyan

## Rationale

_Explain why this task exists or the business driver behind it._

Plan graph_ui de IR (desk/drawer/plans/graph-ui-diccionario-de-componentes), decisiones D7 y D10 de JP del 2026-11-25: UI nueva de specIR con paridad minima con la pagina de spec2viz (U1-U5).

## Goal

_Describe the concrete result this task must produce._

La pestana Anclajes: para un CodeAnchorDoc, la fuente con numeros de linea y el fragmento resaltado; a la derecha el selector, el estado (vigente o cambiado) y los nodos y relaciones de specIR que se apoyan en el.

## Scope

_State what is in scope and what is out of scope._

IR/ui/src/anchors/ y su test. Fuera: Grafo (U6), verificar (U7).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR, app en IR/ui/. Contrato de forma: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md y la maqueta desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html (estructura del prototipo de Kimun, estetica del SLDB Workbench). Decisiones de JP: React con TSX (D10); la app COPIA de sldb/surface lo que necesita y no importa de @sldb/surface (D7), y cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit). Reglas: la UI no calcula, toda escritura es una operacion con nombre por sldb serve, sin datos inventados (si falta un dato se muestra que falta). No tocar sldb/. Tests de componentes con vitest y @testing-library/react; ningun control sin rol y nombre accesible (D3). Los anclajes y sus referentes salen de sldb serve (/document del anchor, /edges o referrers para quien lo usa; ver los routes de serve en sldb). El estado vigente/cambiado es el que sldb ya calcula (anchor_state); la UI no recalcula hashes. Test src/anchors/Anchors.test.tsx con payloads fijos del blog (IR/tests/fixtures): muestra lineas, resalta el fragmento, el estado y la lista de nodos que se apoyan.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/anchors/Anchors.test.tsx

## Done When

_Name the observable condition that makes the task complete._

Anclajes muestra fuente, fragmento, selector, estado y referentes desde sldb serve; su test pasa con tsc.
