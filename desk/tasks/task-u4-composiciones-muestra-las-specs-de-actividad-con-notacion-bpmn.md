---
sldb:
  by: agent
  at: '2026-11-25T06:24:30Z'
  authority: generated
  via: save_document_payload
id: task-u4-composiciones-muestra-las-specs-de-actividad-con-notacion-bpmn
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-u3-composiciones-dibuja-la-receta-elegida-con-su-notacion-zoom-y-arrastre-y-un-nodo-abre-su-document
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
---

# U4: Composiciones muestra las specs de actividad con notacion BPMN

## Rationale

_Explain why this task exists or the business driver behind it._

Plan graph_ui de IR (desk/drawer/plans/graph-ui-diccionario-de-componentes), decisiones D7 y D10 de JP del 2026-11-25: UI nueva de specIR con paridad minima con la pagina de spec2viz (U1-U5).

## Goal

_Describe the concrete result this task must produce._

Que una receta cuya spec es de actividad se dibuje con notacion BPMN, como hacia spec2viz.

## Scope

_State what is in scope and what is out of scope._

IR/ui/src/compositions/ y su test. Fuera: cambios en specIR o sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR, app en IR/ui/. Contrato de forma: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md y la maqueta desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html (estructura del prototipo de Kimun, estetica del SLDB Workbench). Decisiones de JP: React con TSX (D10); la app COPIA de sldb/surface lo que necesita y no importa de @sldb/surface (D7), y cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit). Reglas: la UI no calcula, toda escritura es una operacion con nombre por sldb serve, sin datos inventados (si falta un dato se muestra que falta). No tocar sldb/. Tests de componentes con vitest y @testing-library/react; ningun control sin rol y nombre accesible (D3). La notacion la decide el payload de /notations/view (sldb sabe la notacion de la vista); la UI solo elige el renderizador. Si /notations/view ya devuelve SVG/primitivas para BPMN, reusar el lienzo de U3; si no, dejarlo anotado en result-summary.md como hueco de sldb sin dibujar nada inventado. Test src/compositions/BpmnRecipe.test.tsx con un payload BPMN fijo tomado del store de IR. Revision en frio de johanes (2026-11-25): NO ACTIVAR TODAVIA. sldb no dibuja BPMN; lo hace specIR (src/specir/visual/renderers/bpmn.py y el visor bpmn-js que ya trae). Camino: la extension de D8 (tarea de sldb serve --extension) y una tarea de IR que registre una ruta GET /ext/specir/bpmn/<spec> que devuelva el BPMN XML; la UI lo muestra con el bpmn-js vendorizado en specIR. Esta tarea espera a ambas.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/compositions/BpmnRecipe.test.tsx

## Done When

_Name the observable condition that makes the task complete._

Una receta de actividad se dibuja con BPMN desde /notations/view; su test pasa con tsc.
