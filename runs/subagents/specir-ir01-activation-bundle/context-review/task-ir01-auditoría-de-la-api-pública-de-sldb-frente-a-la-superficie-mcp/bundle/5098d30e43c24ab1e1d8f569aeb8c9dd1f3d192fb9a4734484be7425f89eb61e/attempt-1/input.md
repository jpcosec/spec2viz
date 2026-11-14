FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T03:55:40Z'
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

Auditar estas capacidades con una necesidad acotada: (1) listar/describir modelos y tipos de relación: enumerar modelos y sus campos; (2) leer docs/campos: resolver por la identidad canónica de documento que SLDB ya documente y devolver datos; no inventar otro formato de dirección, y si SLDB no lo define registrar brecha; (3) vecinos/recorridos: seguir aristas entrantes/salientes por profundidad acotada; (4) búsqueda por predicados: buscar documentos por filtros de campo que soporte la API pública existente, sin exigir un lenguaje nuevo; (5) resolver vistas: evaluar una ViewDoc almacenada y devolver el resultado según contrato SLDB, sin fijar formato propio; (6) crear/editar/borrar docs y aristas y escribir RelationTypeDoc/RuleDoc con validación; (7) registrar clases de modelos por código; (8) comprobar integridad; (9) consultar historia/procedencia; (10) detectar una revisión/estado de store utilizable como precondición contra escrituras obsoletas; (11) revertir una escritura aplicada si la API lo permite. Cada fila usa campos fijos: capacidad; necesidad (una frase que explica actor, entrada y resultado requerido, sin diseñar interfaz MCP); estado; evidencia; brecha; acción; referencia de handoff. Estados exactos: disponible (una operación pública cubre la necesidad), requiere-extensión-en-SLDB (hay operaciones públicas relacionadas, pero su composición no puede cumplirla) y faltante (no se encuentra operación pública relacionada en el inventario revisado). Si se cubre con varias operaciones, disponible y acción=componer. Las acciones exactas son usar, componer o solicitar-extensión; disponible usa usar/componer y ambos estados no disponibles usan solicitar-extensión y requieren aparecer en la nota agregada. Citar rutas existentes bajo sldb/src/sldb/api/ y símbolos públicos para disponible; si es composición, citar cada símbolo. Los otros estados enumeran módulos existentes revisados y explican por qué no alcanzan; nunca citan rutas inexistentes. Listar los módulos API y documentos de arquitectura revisados para que la ausencia sea comprobable. Leer pron/source/spec/14-superficie-mcp.md está permitido solo como referencia documental para identificar contratos; no ejecutar ni importar pron, ni usar sus módulos. Si hay alguna fila no disponible, enviar una única nota agregada al desk de SLDB; registrar el ID en la sección Resumen del informe y en cada fila afectada. Si ninguna fila requiere extensión/falta, el Resumen declara que no se envió nota. Fuera: escribir código, modificar SLDB, diseñar tools, usar pron directamente o decidir el contrato final de escritura.

## Implementation Path

_Outline the expected implementation route or affected surface._

Documento de auditoría dentro del repo de specIR. Lectura de sldb/src/sldb/api/ y de la documentación de arquitectura de SLDB; como referencia de contrato, pron/source/spec/14-superficie-mcp.md. Solo si una fila queda como faltante real (no existe ni se puede componer con operaciones públicas existentes), se envía una nota al desk de SLDB con deskops message send; si no hay faltantes, no se envía nada.

## Validation

_List the checks required before this task can close._

- El informe cubre las once capacidades del scope con campos capacidad, necesidad en una frase con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa un estado cerrado y acción permitida; disponible usa usar/componer y cada estado no disponible usa solicitar-extensión.
- Toda capacidad disponible cita ruta existente bajo sldb/src/sldb/api/ y símbolo(s) público(s); una composición nombra todos los símbolos.
- Toda capacidad no disponible lista módulos existentes inspeccionados y explica la insuficiencia sin inventar símbolos o rutas.
- El Resumen del informe declara resultado de la nota agregada: su ID si existe, también en filas afectadas, o que no se envió porque todas las capacidades están disponibles.
- El informe lista fuentes revisadas y no depende de sldb.store, sldb.core ni de importar/ejecutar pron; leer la spec MCP de pron como referencia documental está permitido.

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
- El informe cubre las once capacidades del scope con campos capacidad, necesidad en una frase con actor/entrada/resultado, estado, evidencia, brecha, acción y referencia de handoff.
- Cada fila usa un estado cerrado y acción permitida; disponible usa usar/componer y cada estado no disponible usa solicitar-extensión.
- Toda capacidad disponible cita ruta existente bajo sldb/src/sldb/api/ y símbolo(s) público(s); una composición nombra todos los símbolos.
- Toda capacidad no disponible lista módulos existentes inspeccionados y explica la insuficiencia sin inventar símbolos o rutas.
- El Resumen del informe declara resultado de la nota agregada: su ID si existe, también en filas afectadas, o que no se envió porque todas las capacidades están disponibles.
- El informe lista fuentes revisadas y no depende de sldb.store, sldb.core ni de importar/ejecutar pron; leer la spec MCP de pron como referencia documental está permitido.

