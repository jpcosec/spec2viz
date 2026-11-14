FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:12:08Z'
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

Auditar exactamente 11 filas para el cliente MCP de specIR, con el agente MCP como actor: (1) catálogo de modelos y tipos de relación con campos/tipos; (2) leer payload/campo por identidad estable Model:name; (3) vecinos y recorrido dirigido de aristas con profundidad; (4) seleccionar documentos por predicados con sldb.api.select_documents y hacer búsqueda de texto rankeada con sldb.api.search, registrando si el segundo requiere texto además de where; (5) ejecutar una ViewDoc existente; (6) crear/editar/borrar documentos ordinarios, RelationDoc, RelationTypeDoc y RuleDoc con validación de modelo/reglas; (7) crear modelos con sldb.api.create_model; editar con add_model_field, remove_model_field y edit_model_template, validarlos/promoverlos con validate_model_draft y promote_model_draft; registrar una clase existente con add_model(model_ref=module:ClassName); (8) diagnósticos públicos de integridad del store y del índice de aristas; (9) consultar journal e historial de documento/procedencia; (10) leer StoreFingerprint.store_hash y usar esa huella global como precondición atómica de escritura, rechazando mismatch; (11) revertir escritura confirmada según kb_undo de pron §4. Cada fila corresponde exactamente al número de esta lista; las suboperaciones nombradas se detallan dentro de la fila y no crean filas adicionales. Conducta de undo se limita al archivo ../pron/source/spec/14-superficie-mcp.md §4 y su regla §1 de MoveDoc; si ese texto no permite decidir equivalencia, la fila es no disponible y la pregunta va en la única nota. No considerar disponible precondición global si solo existe source_hash por documento o comparación del caller sin rechazo atómico. Model:name es la identidad estable registrada por SLDB; citar sldb://document/Model:name solo si ../sldb/docs/addressability_model.md lo respalda. Estados exactos: disponible, requiere-extensión-en-SLDB, faltante. Una composición se considera disponible solo si docstring/documento declara expresamente que las operaciones juntas cubren la conducta. Una API relacionada sin conducta suficiente es requiere-extensión-en-SLDB; sin operación relacionada es faltante. Acciones: usar/componer para disponible; solicitar-extensión para las otras. Handoff literal — en todas las filas disponibles; tras una nota, repetir el mismo sldb:<note-id> en cada fila no disponible; si falla el envío, ERROR en cada no disponible. Resumen de éxito exacto: Nota enviada; ID: sldb:<id>. Si todas están disponibles: No se envió nota: todas las capacidades están disponibles. El contrato final de escritura queda fuera. No diseñar tools, escribir código, editar otros repos, importar/ejecutar pron ni leer módulos internos de SLDB.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde /home/jp/proyectos/SLDB_1/IR. El corpus de snapshot es exactamente: todos los archivos Python bajo ../sldb/src/sldb/api/; ../sldb/docs/README.md; ../sldb/docs/addressability_model.md; y estos docs: ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md, selectors.md. Capturar git -C ../sldb rev-parse HEAD y branch --show-current, y git -C ../sldb status --short --untracked-files=all -- para exactamente esas rutas/corpus; el estado de otros archivos del repo no cuenta. Dirty incluye tracked y untracked de esos archivos. Hashear SHA-256 solo los archivos de ese corpus con modificaciones/untracked; excluir IR y ../pron. Si git falla, registrar el resultado y hashear todo el corpus. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md. Inspeccionar recursivamente los archivos Python del API y los docs listados. Para fila 7, add_model(model_ref) registra una clase StructuredNLDoc existente usando referencia module:ClassName; create_model crea/clase desde campos JSON; add_model_field, remove_model_field, edit_model_template, validate_model_draft y promote_model_draft son las operaciones esperadas de edición. Para fila 8 revisar contratos de sldb.api.check_store y check_edges sin ejecutarlos. Para fila 10 verificar si StoreFingerprint.store_hash se acepta y compara dentro de la misma escritura con rechazo atómico. Para fila 4 diferenciar sldb.api.select_documents (predicados) y sldb.api.search (texto rankeado más where); no colapsarlas como una ruta. Leer ../pron/source/spec/14-superficie-mcp.md como único documento externo. Si hay no disponibles, construir message_body con solo esas filas, cada una con número, conducta requerida, rutas/símbolos revisados, brecha, pregunta/solicitud a SLDB y el ID TaskDoc literal task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp. Una pregunta de equivalencia forma parte de esta nota, no de un intercambio previo. Ejecutar una sola vez desde IR: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json. El JSON devuelve el ID; usar ese ID igual como sldb:<id> en todas las filas no disponibles y en el Resumen exacto Nota enviada; ID: sldb:<id>. Si el comando falla o no devuelve ID, handoff ERROR y Resumen exacto con campos Nota no enviada; tarea abierta; Comando: deskops message send "$message_body" --root . --to sldb --kind suggestion --title "[specIR] Brechas API pública SLDB para MCP" --format json; Resultado: <stderr o JSON>; Fecha UTC: <ISO-8601>. No reintentar. Si no hay brechas, handoff literal — y Resumen exacto No se envió nota: todas las capacidades están disponibles. El path ../sldb/... siempre es relativo a la raíz IR citada; el path pron también. No leer módulos internos ni importar/ejecutar pron.

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

