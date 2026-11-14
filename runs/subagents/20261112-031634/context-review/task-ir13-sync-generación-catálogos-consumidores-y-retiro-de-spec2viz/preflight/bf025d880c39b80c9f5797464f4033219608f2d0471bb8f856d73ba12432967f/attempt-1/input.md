FILE:desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
---
sldb:
  by: agent
  at: '2026-11-12T01:35:23Z'
  authority: generated
  via: save_document_payload
id: task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
- task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
- task-ir13c-notaciones-y-paletas-expuestas-desde-specir
- task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/retirement.py
- src/specir/cli.py
- tests/visual/test_retirement_gate.py
- docs/spec2viz/acta-de-retiro.md
- docs/spec2viz/matriz-de-cobertura.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13 Migración de consumidores y gate final de retiro de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Es el cierre de la migración: comprobar que nadie depende ya de spec2viz y que cada capacidad está cubierta. Esta tarea nació como una sola candidata que agrupaba sincronización, catálogos, notaciones, CLI y retiro; se partió para que cada tarea tenga un solo entregable. Las cuatro capacidades quedaron en las tareas IR13a, IR13b, IR13c e IR13d, autoradas desde la misma candidata del drawer, y aquí queda solo el entregable final: la migración de consumidores y el gate de retiro. El tipo task.aggregate no se pudo usar porque el tipo de una tarea no es editable; las dependencias cumplen el papel de agregación.

## Goal

_Describe the concrete result this task must produce._

Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: comprobador del gate de retiro, que lee la matriz de cobertura y verifica que cada fila tiene su condición cumplida con una prueba citada, y que recorre en solo lectura los repos consumidores y los índices de store indicados buscando importaciones o invocaciones de spec2viz y modelos spec2viz.sldb_models; pedidos de migración a los desks de graph_ui, deskops y de cada repo con stores afectados; acta de retiro con la evidencia por fila y por consumidor; actualización de la matriz de cobertura con esa evidencia.
Fuera: implementar capacidades de spec2viz, que corresponden a las tareas de compiladores, renderers, IR13a, IR13b, IR13c e IR13d; editar archivos de otros repos; archivar o borrar el repo spec2viz, que es decisión de su dueño una vez cumplido el gate.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/visual/retirement.py con el comprobador, expuesto como subcomando del comando de specIR; recibe como argumentos las rutas de los repos consumidores y de los stores a revisar y no escribe en ellos. Los cambios en otros repos se piden con deskops message send --to <repo> y se registran en docs/spec2viz/acta-de-retiro.md con la referencia al cambio que los resolvió. La matriz docs/spec2viz/matriz-de-cobertura.md se actualiza con la prueba que acredita cada fila. Propiedad de archivos compartidos: docs/spec2viz/matriz-de-cobertura.md ya existe cuando esta tarea empieza: la crea la tarea de cobertura (IR07). Aquí solo se actualiza, añadiendo por fila la prueba y la evidencia de cumplimiento, después de cerradas IR13a, IR13b, IR13c e IR13d; no se cambian los modos ni las condiciones de retiro que fijó IR07 sin registrarlo en el acta. Propiedad de archivo compartido: src/specir/cli.py lo crea la tarea IR13d con la base del comando y sus subcomandos; esta tarea agrega ahí solo el subcomando del gate de retiro, después de cerrada IR13d, de la que depende, sin modificar los subcomandos existentes.

## Validation

_List the checks required before this task can close._

- El comprobador falla sobre un fixture con una fila de la matriz sin prueba citada y pasa cuando todas la tienen.
- El comprobador detecta una importación de spec2viz y una referencia a spec2viz.sldb_models sembradas en un repo y un índice de store de fixture, y no modifica ningún archivo de ellos.
- Ejecutado sobre los repos reales graph_ui y deskops y sobre los stores inventariados en la matriz, el comprobador no reporta ninguna importación, invocación ni modelo de spec2viz.
- La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz de cobertura.
- El acta de retiro lista, por cada consumidor, el mensaje enviado a su desk y la referencia del cambio que lo resolvió.
- Toda fila de la matriz de cobertura tiene su condición de retiro cumplida y su prueba citada.

## Done When

_Name the observable condition that makes the task complete._

El comprobador pasa sobre los repos y stores reales, el acta de retiro está completa y spec2viz puede archivarse sin que ningún repo del workspace falle.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

