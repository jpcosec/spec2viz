---
sldb:
  by: agent
  at: '2026-11-25T06:07:17Z'
  authority: generated
  via: create_document
id: task-u3-composiciones-dibuja-la-receta-elegida-con-su-notacion-zoom-y-arrastre-y-un-nodo-abre-su-document
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

# U3: Composiciones dibuja la receta elegida con su notacion, zoom y arrastre, y un nodo abre su documento

## Rationale

_Explain why this task exists or the business driver behind it._

Plan graph_ui de IR (desk/drawer/plans/graph-ui-diccionario-de-componentes), decisiones D7 y D10 de JP del 2026-11-25: UI nueva de specIR con paridad minima con la pagina de spec2viz (U1-U5).

## Goal

_Describe the concrete result this task must produce._

Vista previa de la receta elegida dibujada con /notations/view, con zoom, arrastre y reinicio, y clic en un nodo que abre su documento en el panel derecho.

## Scope

_State what is in scope and what is out of scope._

IR/ui/src/compositions/ (vista previa), el lienzo copiado y su test. Fuera: BPMN (U4), notas (U5).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR, app en IR/ui/. Contrato de forma: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md y la maqueta desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html (estructura del prototipo de Kimun, estetica del SLDB Workbench). Decisiones de JP: React con TSX (D10); la app COPIA de sldb/surface lo que necesita y no importa de @sldb/surface (D7), y cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit). Reglas: la UI no calcula, toda escritura es una operacion con nombre por sldb serve, sin datos inventados (si falta un dato se muestra que falta). No tocar sldb/. Tests de componentes con vitest y @testing-library/react; ningun control sin rol y nombre accesible (D3). Copiar surface/src/workbench/NotationSvgCanvas.tsx (citando origen) y usarlo con el payload de /notations/view. El documento del nodo sale de /document. Zoom y reinicio como botones con nombre accesible. Test src/compositions/RecipePreview.test.tsx con payloads fijos: dibuja, zoom cambia la escala, reiniciar vuelve, clic en nodo pide /document y lo muestra en el panel.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/compositions/RecipePreview.test.tsx

## Done When

_Name the observable condition that makes the task complete._

RecipePreview dibuja la receta, hace zoom/arrastre/reinicio y abre el documento del nodo; su test pasa con tsc.
