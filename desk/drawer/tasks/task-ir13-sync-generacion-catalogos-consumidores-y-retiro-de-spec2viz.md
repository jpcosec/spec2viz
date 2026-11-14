---
id: task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz
status: deferred
summary: 'Candidata diferida: cubrir la sincronización al store, la generación de
  specs, los catálogos y las notaciones; migrar a los consumidores y cumplir el gate
  de retiro de spec2viz.'
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ''
history: []
references: []
depends_on:
- task-ir07-matriz-de-cobertura-de-spec2viz-para-su-retiro
- task-ir11-compiladores-y-proyecciones-de-spec2viz
- task-ir12-renderers-linter-y-recursos-estaticos-de-spec2viz
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
---

# IR13 Sync, generación, catálogos, consumidores y retiro de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Candidata diferida. Es el cierre de la migración: lo que conecta los diagramas con el store, lo que consumen graph_ui y deskops, y la comprobación final de que nadie depende ya de spec2viz.

## Goal

_Describe the concrete result this task must produce._

specIR cubre el resto de las capacidades de spec2viz, sus consumidores usan specIR o SLDB, y el gate de retiro de la candidata de cobertura se cumple.

## Scope

_State what is in scope and what is out of scope._

Dentro: SpecSync (spec a SpecDoc, SpecNodeDoc y RelationDoc, con creación del RelationTypeDoc que falte y borrado de lo que salió del spec); from-graph (grafo o snapshot a spec de componentes); generación de spec de componentes desde AST de Python; catálogos: build, sync, validate y serve con autoguardado de anotaciones, registro vistas.yml y stores jerárquicos; emparejamiento de átomos y cobertura por vista; NotationDoc, GlyphDoc, LinkDoc y PaletteDoc: list, validate, sync y view, expuestos desde specIR sobre lo que ya vive en SLDB; CLI, API Python pública y habilidades de agente equivalentes; migración de consumidores: graph_ui, deskops y stores cuyo índice registra modelos spec2viz.sldb_models; gate final de retiro.
Fuera: retirar spec2viz mientras alguna fila de la matriz de cobertura tenga su condición sin cumplir. Los cambios en graph_ui, deskops o SLDB se piden por el desk de cada repo; esta candidata no los edita desde specIR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.code (el tipo se asigna al autorar la tarea activa con deskops add task --task-type; en una candidata diferida task_type queda vacío); por su tamaño, al autorarla puede partirse en varias tareas activas siguiendo los grupos de filas de la matriz de cobertura. Sincronización y notaciones por la API pública de SLDB; paridad medida con las pruebas de spec2viz de sync, catálogo, notación y átomos, y con las pruebas de notación de graph_ui; coordinación con los otros repos por mensajes entre desks.

## Validation

_List the checks required before this task can close._

- Sincronizar un spec con specIR deja en el store los mismos SpecDoc, SpecNodeDoc y RelationDoc que spec2viz, y volver a sincronizar tras quitar un elemento borra su documento.
- from-graph y la generación desde AST producen en specIR un spec de componentes equivalente al de spec2viz sobre los fixtures, o su reemplazo por proyección tiene la prueba equivalente declarada.
- catalog build, sync, validate y serve tienen equivalente en specIR: mismos errores tipados en validate, mismo contenido de store tras sync, y las anotaciones hechas en serve se guardan.
- list, validate, sync y view de notaciones y list, validate y sync de paletas responden desde specIR, incluida la comprobación de contraste.
- Ningún archivo de graph_ui ni de deskops importa o invoca spec2viz (búsqueda en ambos repos).
- Ningún índice de store registra un modelo spec2viz.sldb_models.
- La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz de cobertura.
- Toda fila de la matriz de cobertura tiene su condición de retiro cumplida.

## Done When

_Name the observable condition that makes the task complete._

El gate de retiro de la candidata de cobertura se cumple completo y spec2viz puede archivarse sin que ningún repo del workspace falle.
