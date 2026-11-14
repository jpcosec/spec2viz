FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:02:54Z'
  authority: generated
  via: save_document_payload
id: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:mcp
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/auditoria/sldb-api-frente-a-mcp.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
from_drawer: desk/drawer/tasks/task-ir01-auditor-a-de-la-api-p-blica-de-sldb-frente-a-la-superficie-mcp.md
---

# IR01 Auditoría de la API pública de SLDB frente a la superficie MCP

## Rationale

_Explain why this task exists or the business driver behind it._

Antes de diseñar la superficie MCP de specIR hay que saber qué ofrece ya la API pública de SLDB, para no reimplementar en specIR lo que es general y no depender de módulos internos de SLDB ni de pron.

## Goal

_Describe the concrete result this task must produce._

Una matriz que diga, capacidad por capacidad, qué necesita la superficie MCP de specIR y si la API pública de SLDB ya lo ofrece, hay que extenderlo en SLDB, o falta.

## Scope

_State what is in scope and what is out of scope._

Matriz para el cliente MCP de specIR; el actor de cada fila es el agente MCP. Auditar exactamente estas necesidades: (1) catálogo de modelos y tipos de relación, con campos/tipos; (2) leer payload por identidad estable Model:name y campo; (3) vecinos y recorrido dirigido de aristas con profundidad; (4) buscar documentos por filtros de campo en la sintaxis existente de sldb.api.where/search, sin pedir filtros que SLDB no documenta; (5) ejecutar una ViewDoc existente y obtener su resultado; (6) crear, editar y borrar documentos y RelationDoc/RelationTypeDoc/RuleDoc con las validaciones del modelo/reglas; (7) crear/editar modelos según el nivel 3 de pron §4, y registrar/promover modelos Python ya definidos; (8) revisar integridad del store e índice de aristas; (9) consultar journal e historial de documento con procedencia; (10) leer una huella/estado del store y aplicarla como precondición atómica de escritura, rechazando el cambio si el estado esperado ya no coincide; (11) revertir escritura confirmada según el contrato kb_undo de pron §4. El contrato normativo de undo es exactamente la forma undo de pron §4 y la regla de §1 de que escrituras por forma dejan MoveDoc; no inferir semántica adicional. Si ese contrato no permite decidir si SLDB lo soporta, registrar la ambigüedad de contrato y solicitar aclaración en la nota al desk de SLDB; no inventar comportamiento. No considerar disponible una capacidad de concurrencia si solo se compara en el llamador antes de escribir y la operación no rechaza estado obsoleto atómicamente. Identidad Model:name es el nombre estable que SLDB registra al crear/trackear un doc; usar la documentación existente de sldb://document/Model:name solo cuando respalde la identidad y citar el argumento que aceptan las operaciones. Los filtros auditados son los predicados ya definidos por sldb.api.where; si la API de búsqueda exige texto además del filtro, documentar esa limitación. La necesidad describe la conducta requerida, no una firma de futura tool. Estado disponible solo si la conducta exacta está en la API pública directamente o por composición documentada; si hay API relacionada pero falta comportamiento, requiere-extensión-en-SLDB; si no hay operación relacionada, faltante. Acciones exactas: usar/componer para disponible; solicitar-extensión para estados no disponibles. Referencia handoff literal — para toda fila disponible y sldb:<note-id> para cada no disponible, referidas a una única nota. La raya es el carácter EM DASH literal. El informe contiene una sección llamada Resumen donde se declara ID o ausencia de nota. Inspeccionar recursivamente todos los archivos Python bajo ../sldb/src/sldb/api/ y el corpus de Implementation Path. La ausencia se justifica contra ese corpus exacto. Leer ../pron/source/spec/14-superficie-mcp.md solo como referencia documental; no importar/ejecutar pron ni abrir código fuera de sldb.api. Fuera: diseñar tools, escribir código, editar otros repos y decidir el contrato final de escritura.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR; todas las rutas relativas parten de esa raíz y se inspecciona el working tree presente, no una versión implícita. Antes de leer, registrar en el informe el commit y branch de ../sldb si existen, el resultado de git status --short y la fecha UTC; si los archivos auditados tienen modificaciones sin commit, registrar hashes SHA-256 de todos los archivos Python inspeccionados y documentos listados para fijar el snapshot. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md (crear docs/auditoria si falta). Inspeccionar recursivamente todos los archivos Python bajo ../sldb/src/sldb/api/, ../sldb/docs/README.md, ../sldb/docs/addressability_model.md y ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md y selectors.md. Leer ../pron/source/spec/14-superficie-mcp.md como único documento externo de contrato MCP. Si al menos una fila no está disponible, enviar un mensaje único a sldb cuyo título sea [specIR] Brechas API pública SLDB para MCP y cuerpo enumere por fila: capacidad/necesidad, rutas y símbolos revisados, conducta faltante, pregunta de contrato para el equipo propietario y referencia TaskDoc IR01. No proponer decisión cerrada para el equipo dueño. Registrar el ID devuelto como sldb:<id> en la sección Resumen y las filas afectadas. Si ninguna es no disponible, poner el carácter literal — en todas las referencias y declarar en Resumen que no se envió nota. Si el envío falla o no devuelve ID, registrar comando, resultado/error y fecha en Resumen, dejar el informe escrito y no cerrar la tarea ni marcar la brecha como notificada; no reintentar automáticamente. No leer módulos internos de SLDB ni importar/ejecutar pron.

## Validation

_List the checks required before this task can close._

- El informe contiene exactamente once capacidades y cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa uno de los estados cerrados y la acción correspondiente; disponible usa usar/componer y cada no disponible usa solicitar-extensión.
- Una fila disponible cita ruta existente bajo sldb/src/sldb/api/ y todos los símbolos públicos; la composición nombra cada operación.
- Cada fila no disponible enumera módulos existentes inspeccionados y explica la conducta que falta; no cita rutas o símbolos inventados.
- El informe lista el snapshot: commit/branch de sldb si existen, fecha UTC y git status; si los archivos de fuente están modificados, incluye hashes SHA-256 para fijar la revisión auditada.
- Si hay filas no disponibles, se envió un único mensaje cuyo título y cuerpo siguen Implementation Path, y el ID exacto aparece en Resumen y filas afectadas; si no hay filas no disponibles, Resumen declara que no se envió nota y cada handoff disponible contiene el carácter literal —.
- Si deskops message send falla o no retorna ID, Resumen registra el resultado y la tarea no se cierra como notificada.
- El informe lista fuentes revisadas y no abre módulos internos de SLDB ni importa/ejecuta pron; leer la spec pron como documento está permitido.

## Done When

_Name the observable condition that makes the task complete._

La matriz está escrita, cada fila tiene estado y cita, y los faltantes reales (si los hay) están notificados a SLDB.

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

FILE:desk/atoms/atom-specir-no-depende-de-pron-adopta-contratos-no-código.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:33Z'
  authority: generated
  via: create_document
id: atom-specir-no-depende-de-pron-adopta-contratos-no-código
title: 'specIR no depende de pron: adopta contratos, no código'
five_wh_one_plus: how_not
tags:
- system:specir
- system:pron
- topic:dependencias
---

# specIR no depende de pron: adopta contratos, no código

## Answer

specIR no usa pron como base ni como dependencia: ningún import de pron y ninguna entrada suya en las dependencias del paquete. De la superficie MCP de pron (pron/source/spec/14-superficie-mcp.md) se pueden adoptar contratos reimplementados sobre SLDB: direcciones por URI, paginación con total y truncated, selectores que solo resuelven lo que el store declara, dry_run en toda escritura, niveles de mutabilidad y cero texto libre en el camino de la escritura. No se adoptan las formas, el léxico, las sesiones de diálogo ni el concepto de mundo. Decisión del dueño del proyecto, 2026-11-11: pron está desactualizado y no funciona bien como base.

FILE:instruccion
Cold-bundle de la tarea task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- El informe contiene exactamente once capacidades y cada fila incluye capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa uno de los estados cerrados y la acción correspondiente; disponible usa usar/componer y cada no disponible usa solicitar-extensión.
- Una fila disponible cita ruta existente bajo sldb/src/sldb/api/ y todos los símbolos públicos; la composición nombra cada operación.
- Cada fila no disponible enumera módulos existentes inspeccionados y explica la conducta que falta; no cita rutas o símbolos inventados.
- El informe lista el snapshot: commit/branch de sldb si existen, fecha UTC y git status; si los archivos de fuente están modificados, incluye hashes SHA-256 para fijar la revisión auditada.
- Si hay filas no disponibles, se envió un único mensaje cuyo título y cuerpo siguen Implementation Path, y el ID exacto aparece en Resumen y filas afectadas; si no hay filas no disponibles, Resumen declara que no se envió nota y cada handoff disponible contiene el carácter literal —.
- Si deskops message send falla o no retorna ID, Resumen registra el resultado y la tarea no se cierra como notificada.
- El informe lista fuentes revisadas y no abre módulos internos de SLDB ni importa/ejecuta pron; leer la spec pron como documento está permitido.

