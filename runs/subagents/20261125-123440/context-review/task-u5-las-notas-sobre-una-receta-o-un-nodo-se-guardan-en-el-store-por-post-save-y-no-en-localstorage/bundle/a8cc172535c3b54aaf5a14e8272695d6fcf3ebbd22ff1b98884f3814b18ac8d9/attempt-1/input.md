FILE:desk/tasks/task-u5-las-notas-sobre-una-receta-o-un-nodo-se-guardan-en-el-store-por-post-save-y-no-en-localstorage.md
---
sldb:
  by: agent
  at: '2026-11-25T06:24:37Z'
  authority: generated
  via: save_document_payload
id: task-u5-las-notas-sobre-una-receta-o-un-nodo-se-guardan-en-el-store-por-post-save-y-no-en-localstorage
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

# U5: las notas sobre una receta o un nodo se guardan en el store por POST /save y no en localStorage

## Rationale

_Explain why this task exists or the business driver behind it._

Plan graph_ui de IR (desk/drawer/plans/graph-ui-diccionario-de-componentes), decisiones D7 y D10 de JP del 2026-11-25: UI nueva de specIR con paridad minima con la pagina de spec2viz (U1-U5).

## Goal

_Describe the concrete result this task must produce._

Notas sobre la receta o el nodo, guardadas en el store de sldb (como las anotaciones de spec2viz, pero en el store), con lista, alta y edicion.

## Scope

_State what is in scope and what is out of scope._

IR/ui/src/notes/ y su test. Fuera: modelos nuevos en sldb o specIR (si hace falta un modelo de nota, usar uno existente del store y anotarlo).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR, app en IR/ui/. Contrato de forma: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md y la maqueta desk/drawer/plans/graph-ui-diccionario-de-componentes/maqueta-ui.html (estructura del prototipo de Kimun, estetica del SLDB Workbench). Decisiones de JP: React con TSX (D10); la app COPIA de sldb/surface lo que necesita y no importa de @sldb/surface (D7), y cada archivo copiado lleva un comentario de cabecera con su origen (ruta en sldb y commit). Reglas: la UI no calcula, toda escritura es una operacion con nombre por sldb serve, sin datos inventados (si falta un dato se muestra que falta). No tocar sldb/. Tests de componentes con vitest y @testing-library/react; ningun control sin rol y nombre accesible (D3). Escritura solo por POST /save de sldb serve con expected (control optimista) como hace surface; nada en localStorage. Elegir el modelo de nota que ya exista en el store de IR (revisar /schema); si no hay ninguno adecuado, parar y anotarlo en result-summary.md en vez de inventar uno. Test src/notes/Notes.test.tsx con fetch mockeado: lista, alta manda POST /save con el payload esperado, un 409 muestra el conflicto. Revision en frio de johanes (2026-11-25): el modelo ya existe: CatalogAnnotationsDoc (src/specir/visual/catalog/annotations.py:25-28), registrado con add_model como ya hace annotations.py; usar ese y no buscar otro en /schema, para que las notas de la UI y las de la pagina de catalog build (D9) sean las mismas.

## Validation

_List the checks required before this task can close._

- cd ui && npx tsc --noEmit && npx vitest run src/notes/Notes.test.tsx

## Done When

_Name the observable condition that makes the task complete._

Las notas se listan y se guardan por POST /save con expected; su test pasa con tsc.

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
Cold-bundle de la tarea task-u5-las-notas-sobre-una-receta-o-un-nodo-se-guardan-en-el-store-por-post-save-y-no-en-localstorage: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd ui && npx tsc --noEmit && npx vitest run src/notes/Notes.test.tsx

