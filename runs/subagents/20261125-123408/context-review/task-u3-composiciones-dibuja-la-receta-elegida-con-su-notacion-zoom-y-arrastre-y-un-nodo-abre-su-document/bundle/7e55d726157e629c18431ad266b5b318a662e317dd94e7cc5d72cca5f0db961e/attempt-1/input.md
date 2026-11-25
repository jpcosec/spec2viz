FILE:desk/tasks/task-u3-composiciones-dibuja-la-receta-elegida-con-su-notacion-zoom-y-arrastre-y-un-nodo-abre-su-document.md
---
sldb:
  by: agent
  at: '2026-11-25T06:25:03Z'
  authority: generated
  via: save_document_payload
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


Repo /mnt/ssd/proyectos/SLDB_1/IR, app en IR/ui/. Contrato de forma: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md y la maqueta desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html (estructura del prototipo de Kimun, estetica del SLDB Workbench). Decisiones de JP: React con TSX (D10); la app COPIA de sldb/surface lo que necesita y no importa de @sldb/surface (D7), y cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit). Reglas: la UI no calcula, toda escritura es una operacion con nombre por sldb serve, sin datos inventados (si falta un dato se muestra que falta). No tocar sldb/. Tests de componentes con vitest y @testing-library/react; ningun control sin rol y nombre accesible (D3). Copiar surface/src/workbench/NotationSvgCanvas.tsx (citando origen) y usarlo con el payload de /notations/view. El documento del nodo sale de /document. Zoom y reinicio como botones con nombre accesible. Test src/compositions/RecipePreview.test.tsx con payloads fijos: dibuja, zoom cambia la escala, reiniciar vuelve, clic en nodo pide /document y lo muestra en el panel. Aceptacion contra datos reales: el store de IR no tiene SpecDoc ni ViewDoc; el de pron (/mnt/ssd/proyectos/SLDB_1/pron/.sldb) tiene 15 SpecDoc. sldb serve --store <store de pron> para la prueba manual.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/compositions/RecipePreview.test.tsx

## Done When

_Name the observable condition that makes the task complete._

RecipePreview dibuja la receta, hace zoom/arrastre/reinicio y abre el documento del nodo; su test pasa con tsc. Ademas, una captura en Chrome real de una spec de pron dibujada por el lienzo copiado, guardada en el run dir y citada en result-summary.md.

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
Cold-bundle de la tarea task-u3-composiciones-dibuja-la-receta-elegida-con-su-notacion-zoom-y-arrastre-y-un-nodo-abre-su-document: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd ui && npx tsc --noEmit && npx vitest run src/compositions/RecipePreview.test.tsx

