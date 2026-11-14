FILE:desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
---
sldb:
  by: agent
  at: '2026-11-12T03:23:29Z'
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

Dentro: comprobador del gate de retiro, que lee la matriz de cobertura y verifica que cada fila tiene su condición cumplida con una prueba citada, y que recorre en solo lectura el universo auditado buscando dependencias de spec2viz. Universo auditado: exactamente los repos consumidores y los stores que lista el inventario de consumidores de docs/spec2viz/matriz-de-cobertura.md, más el propio repo de specIR; un repo o store que no esté en ese inventario no se audita, y añadir uno exige actualizar primero el inventario. Qué cuenta como dependencia: importaciones de spec2viz en código (import spec2viz o from spec2viz); dependencias declaradas en configuración ejecutable (pyproject.toml, requirements, archivos de CI, Makefile y scripts); puntos de entrada y llamadas al comando spec2viz en código, scripts o configuración ejecutable; llamadas a su API Python; y modelos spec2viz.sldb_models registrados en un índice de store. Qué no cuenta: menciones en texto, documentación, comentarios, changelogs o documentos del desk. Salida: por cada dependencia remanente, el repo o store, la ruta del archivo, la línea y la clase de dependencia; con al menos una, el gate falla con código de salida distinto de cero y el retiro no se puede declarar; pedidos de migración a los desks de graph_ui, deskops y de cada repo con stores afectados; acta de retiro con la evidencia por fila y por consumidor; actualización de la matriz de cobertura con esa evidencia.
Fuera: implementar capacidades de spec2viz, que corresponden a las tareas de compiladores, renderers, IR13a, IR13b, IR13c e IR13d; editar archivos de otros repos; archivar o borrar el repo spec2viz, que es decisión de su dueño una vez cumplido el gate.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/visual/retirement.py con el comprobador, expuesto como subcomando del comando de specIR; lee del inventario de la matriz de cobertura la lista de repos consumidores y de stores a revisar y recibe por argumento solo la ruta local de cada uno; no escribe en ellos. Si el gate falla, el acta registra las dependencias remanentes con su ruta y línea y deja el retiro como no declarado. Los cambios en otros repos se piden con deskops message send --to <repo> y se registran en docs/spec2viz/acta-de-retiro.md con la referencia al cambio que los resolvió. La matriz docs/spec2viz/matriz-de-cobertura.md se actualiza con la prueba que acredita cada fila. Propiedad de archivos compartidos: docs/spec2viz/matriz-de-cobertura.md ya existe cuando esta tarea empieza: la crea la tarea de cobertura (IR07). Aquí solo se actualiza, añadiendo por fila la prueba y la evidencia de cumplimiento, después de cerradas IR13a, IR13b, IR13c e IR13d; no se cambian los modos ni las condiciones de retiro que fijó IR07 sin registrarlo en el acta. Propiedad de archivo compartido: src/specir/cli.py lo crea la tarea IR13d con la base del comando y sus subcomandos; esta tarea agrega ahí solo el subcomando del gate de retiro, después de cerrada IR13d, de la que depende, sin modificar los subcomandos existentes.

## Validation

_List the checks required before this task can close._

- El comprobador falla sobre una matriz de entrada con una fila sin prueba citada y pasa cuando todas la tienen.
- Sobre un repo de entrada con una importación de spec2viz en código, una dependencia en pyproject.toml y una llamada al comando spec2viz en un script, y un índice de store con un modelo spec2viz.sldb_models, el comprobador reporta las cuatro con repo, ruta, línea y clase de dependencia, termina con código de salida distinto de cero y no modifica ningún archivo.
- Sobre un repo de entrada que solo menciona spec2viz en documentación, comentarios y un changelog, el comprobador no reporta ninguna dependencia.
- El comprobador audita exactamente los repos y stores del inventario de la matriz de cobertura más el repo de specIR, y falla con un error que lo dice si se le pide auditar uno que no está en el inventario o si falta la ruta de uno que sí está.
- Ejecutado sobre todos los repos y stores reales del inventario, el comprobador no reporta ninguna dependencia y termina con código de salida cero.
- La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz de cobertura.
- El acta de retiro lista, por cada consumidor del inventario, el mensaje enviado a su desk, la referencia del cambio que lo resolvió y la salida del comprobador; si quedó alguna dependencia, el acta dice que el retiro no está declarado.
- Toda fila de la matriz de cobertura tiene su condición de retiro cumplida y su prueba citada.

## Done When

_Name the observable condition that makes the task complete._

El comprobador termina con código de salida cero sobre todo el universo auditado, el acta de retiro está completa y declara el retiro, y spec2viz puede archivarse sin que ningún repo del workspace falle.

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

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

FILE:desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas
status: active
summary: Cómo se acredita la cobertura de una capacidad de spec2viz.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: la paridad con spec2viz se demuestra con sus pruebas

## What

_Define the context or guardrail this pill carries._

Una capacidad de spec2viz se considera cubierta solo cuando la prueba o golden correspondiente de spec2viz pasa contra specIR, o cuando su fila de la matriz de cobertura declara un reemplazo con una prueba equivalente que pasa.

## Why

_Explain why this context matters for safe execution._

El objetivo es retirar spec2viz; declarar paridad sin prueba dejaría funcionalidades perdidas al retirarlo.

## When

_Describe when an agent should apply this pill._

En toda tarea que migre o reemplace una capacidad de spec2viz, y al evaluar el gate de retiro.

## Where

_Name the files, surfaces, or scope this pill applies to._

tests/visual/ en specIR; como referencia de solo lectura, spec2viz/tests/ y la matriz docs/spec2viz/matriz-de-cobertura.md.

## How

_Describe the correct way to apply this guidance._

Portar los fixtures y golden de spec2viz a tests/ de specIR y ejecutarlos; registrar en la matriz, por fila, la prueba que acredita la cobertura.

## How Not

_Describe the shortcut or failure mode to avoid._

No declarar una fila como cubierta porque otra herramienta la sustituya de hecho; no descartar una capacidad por falta de uso; no modificar un golden para que la prueba pase.

FILE:desk/atoms/atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:35Z'
  authority: generated
  via: create_document
id: atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
title: specIR reemplaza a spec2viz y cubre todas sus funciones
five_wh_one_plus: when
tags:
- system:specir
- system:spec2viz
- topic:migracion
---

# specIR reemplaza a spec2viz y cubre todas sus funciones

## Answer

spec2viz nació aparte porque SLDB no tenía grafos; ahora los tiene. specIR incorporará la capa visual y debe cubrir todas las funcionalidades de spec2viz; cuando las cubra, spec2viz se retira. Ninguna funcionalidad se da por descartada porque otra herramienta la sustituya de hecho: cada una se cubre migrándola tal cual, reemplazándola por otra arquitectura o experiencia con resultado equivalente, o exponiendo desde specIR lo que ya vive en SLDB. En los tres casos specIR responde por el camino de retiro. No es un consumidor permanente de spec2viz. Decisión del dueño del proyecto, 2026-11-11.

FILE:desk/atoms/atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:36Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
title: El vocabulario visual y el resolvedor de vistas ya viven en SLDB
five_wh_one_plus: where
tags:
- system:specir
- system:sldb
- system:spec2viz
- topic:vistas
- layer:modelo
provenance: ../sldb-astryx/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/dag.yaml
---

# El vocabulario visual y el resolvedor de vistas ya viven en SLDB

## Answer

Desde el plan absorber-spec2viz-y-modelos-ui de SLDB (entregado el 2026-11-07), los modelos SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb/src/sldb/models/notation/, las notaciones y paletas builtin en sldb/src/sldb/notations/, y el resolvedor de vistas y proyecciones en sldb/src/sldb/api/notations/. Un alias en sldb/src/sldb/api/model_registry/model_reference.py resuelve las referencias antiguas spec2viz.sldb_models. specIR usa esas piezas desde SLDB y no las redefine. En spec2viz quedan, sin equivalente en SLDB, la autoría de specs YAML, los compiladores, los renderizadores, el catálogo y la sincronización de specs al store.

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:instruccion
Cold-bundle de la tarea task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- El comprobador falla sobre una matriz de entrada con una fila sin prueba citada y pasa cuando todas la tienen.
- Sobre un repo de entrada con una importación de spec2viz en código, una dependencia en pyproject.toml y una llamada al comando spec2viz en un script, y un índice de store con un modelo spec2viz.sldb_models, el comprobador reporta las cuatro con repo, ruta, línea y clase de dependencia, termina con código de salida distinto de cero y no modifica ningún archivo.
- Sobre un repo de entrada que solo menciona spec2viz en documentación, comentarios y un changelog, el comprobador no reporta ninguna dependencia.
- El comprobador audita exactamente los repos y stores del inventario de la matriz de cobertura más el repo de specIR, y falla con un error que lo dice si se le pide auditar uno que no está en el inventario o si falta la ruta de uno que sí está.
- Ejecutado sobre todos los repos y stores reales del inventario, el comprobador no reporta ninguna dependencia y termina con código de salida cero.
- La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz de cobertura.
- El acta de retiro lista, por cada consumidor del inventario, el mensaje enviado a su desk, la referencia del cambio que lo resolvió y la salida del comprobador; si quedó alguna dependencia, el acta dice que el retiro no está declarado.
- Toda fila de la matriz de cobertura tiene su condición de retiro cumplida y su prueba citada.

