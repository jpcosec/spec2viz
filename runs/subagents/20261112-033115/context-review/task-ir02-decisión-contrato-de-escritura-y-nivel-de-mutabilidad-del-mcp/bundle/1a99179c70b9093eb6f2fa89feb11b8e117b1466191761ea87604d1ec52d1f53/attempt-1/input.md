FILE:desk/tasks/task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T03:23:12Z'
  authority: generated
  via: save_document_payload
id: task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
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
depends_on:
- task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp
pills:
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/decisiones/contrato-de-escritura-mcp.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir02-decisi-n-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp.md
---

# IR02 Decisión: contrato de escritura y nivel de mutabilidad del MCP

## Rationale

_Explain why this task exists or the business driver behind it._

La superficie MCP promete proponer, validar y aplicar como pasos separados, pero no está decidido con qué mecanismo ni quién limita hasta dónde puede escribir un agente. Sin esa decisión la escritura por MCP no se puede diseñar.

## Goal

_Describe the concrete result this task must produce._

Un registro de decisión en docs/decisiones/contrato-de-escritura-mcp.md con cuatro decisiones tomadas por el dueño del proyecto (qué es una propuesta de cambio, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido, y si existe deshacer), y un atom durable por cada decisión que la deja disponible para las demás tareas.

## Scope

_State what is in scope and what is out of scope._

Dentro: (a) propuesta de cambio como lote prevalidado sin persistir o como documento persistente; (b) precondición que impide aplicar sobre un store que cambió desde la validación; (c) dónde se declara el nivel de escritura permitido (contenido, reglas y tipos de relación, modelos): al arrancar el servidor, en un documento del store, o por actor; (d) si hay una operación de deshacer o basta la historia en git. Fuera: implementar; decidir permisos multiusuario.

## Implementation Path

_Outline the expected implementation route or affected surface._

El entregable tiene dos partes con un solo origen. (1) Registro de decisión: docs/decisiones/contrato-de-escritura-mcp.md, con una sección por decisión que contiene el contexto, las alternativas, la operación de la API pública de SLDB que sostiene cada alternativa según la matriz de la tarea de auditoría, la alternativa elegida, el motivo y la fecha. Es el documento con el que cierra esta tarea. (2) Cuatro atoms, uno por decisión, creados con deskops add atom con --provenance docs/decisiones/contrato-de-escritura-mcp.md; cada atom enuncia solo la decisión vigente y el registro conserva las alternativas descartadas. Quién hace qué: el ejecutor redacta el registro con las alternativas y una recomendación; el dueño del proyecto elige, y su elección queda escrita en el registro (el recibo owner que exige la activación de una tarea de decisión acredita que la decisión es suya); el ejecutor crea después los cuatro atoms y actualiza con deskops edit atom el atom de principios de seguridad de la superficie MCP para que cite los mecanismos decididos; los ids de los atoms creados se anotan en el registro y en las referencias de la tarea. Si el registro cambia más adelante, se actualiza primero el registro y después el atom correspondiente, nunca al revés.

## Validation

_List the checks required before this task can close._

- docs/decisiones/contrato-de-escritura-mcp.md existe y tiene una sección por cada una de las cuatro decisiones, cada una con alternativas, alternativa elegida, motivo, fecha y quién decidió.
- Cada sección nombra la operación de la API pública de SLDB que sostiene la alternativa elegida según la matriz de auditoría, o la carencia notificada a SLDB.
- Existe un atom por cada decisión, su campo provenance apunta al registro y su texto coincide con la alternativa elegida en el registro.
- El registro lista los ids de los cuatro atoms y las referencias de la tarea los incluyen.
- Ninguna decisión introduce un camino de escritura al store que no pase por la API pública de SLDB.
- El atom de principios de seguridad de la superficie MCP cita los mecanismos decididos y ya no los declara pendientes.

## Done When

_Name the observable condition that makes the task complete._

El registro de decisión está completo con la elección del dueño, los cuatro atoms existen y apuntan a él, y la tarea de escritura por MCP puede citar un mecanismo concreto para cada principio.

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

FILE:desk/atoms/atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir.md
---
sldb:
  by: agent
  at: '2026-11-12T00:48:16Z'
  authority: generated
  via: save_document_payload
id: atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
title: Principios de seguridad de la superficie MCP de specIR
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- topic:procedencia
- layer:superficie
provenance: fundamentos_modelado_semantico_mcp.md
---

# Principios de seguridad de la superficie MCP de specIR

## Answer

La superficie MCP sigue estos principios: las consultas no tienen efectos laterales; proponer, validar y aplicar una modificación son pasos separados; no se aplica un cambio sobre un estado que ya no es el que se validó; cada nodo y relación declara su procedencia y una inferencia de un LLM nunca pasa a hecho validado en silencio; los límites de escritura los impone el servidor, no el agente ni la interfaz; el sistema conserva lo que desconoce en vez de rellenarlo. Son principios, no mecanismos: cómo se representa una propuesta, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido y qué taxonomía de procedencia se usa están pendientes de decisión en las candidatas de contrato de escritura y de procedencia.

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
Cold-bundle de la tarea task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- docs/decisiones/contrato-de-escritura-mcp.md existe y tiene una sección por cada una de las cuatro decisiones, cada una con alternativas, alternativa elegida, motivo, fecha y quién decidió.
- Cada sección nombra la operación de la API pública de SLDB que sostiene la alternativa elegida según la matriz de auditoría, o la carencia notificada a SLDB.
- Existe un atom por cada decisión, su campo provenance apunta al registro y su texto coincide con la alternativa elegida en el registro.
- El registro lista los ids de los cuatro atoms y las referencias de la tarea los incluyen.
- Ninguna decisión introduce un camino de escritura al store que no pase por la API pública de SLDB.
- El atom de principios de seguridad de la superficie MCP cita los mecanismos decididos y ya no los declara pendientes.

