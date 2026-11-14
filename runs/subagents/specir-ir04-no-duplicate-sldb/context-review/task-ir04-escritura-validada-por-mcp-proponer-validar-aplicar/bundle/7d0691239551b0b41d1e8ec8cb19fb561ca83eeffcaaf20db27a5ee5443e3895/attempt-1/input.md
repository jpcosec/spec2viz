FILE:desk/tasks/task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar.md
---
sldb:
  by: agent
  at: '2026-11-12T04:40:28Z'
  authority: generated
  via: save_document_payload
id: task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar
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
- task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
- task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- src/specir/mcp/write_tools.py
- src/specir/mcp/changes.py
- src/specir/mcp/mutability.py
- tests/mcp/test_write_tools.py
- tests/mcp/test_dry_run.py
- tests/mcp/test_mutability.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar.md
---

# IR04 Escritura validada por MCP: proponer, validar, aplicar

## Rationale

_Explain why this task exists or the business driver behind it._

Un agente que solo lee no desbloquea el modelado. La escritura por MCP tiene que impedir que el modelo quede inconsistente y dejar rastro de quién escribió qué.

## Goal

_Describe the concrete result this task must produce._

Tools MCP de escritura con las que un agente propone, valida y aplica cambios al store, con el mecanismo decidido en la tarea de contrato de escritura.

## Scope

_State what is in scope and what is out of scope._

_State what is in scope and what is out of scope._

Dentro, mutaciones del store que expone el MCP: crear, editar y borrar documentos de modelos ya registrados; afirmar y retirar aristas (RelationDoc); declarar y editar tipos de relación (RelationTypeDoc) y reglas (RuleDoc), que son documentos del store y por eso se escriben como datos. Toda escritura admite ejecución en seco. Fuera: crear o editar clases Python de modelos por MCP. Las clases de modelo se definen como código en el paquete specIR (o en el paquete del proyecto que las declare) y entran al store por el registro de modelos de SLDB; exponer su edición por MCP queda como decisión posterior, condicionada a la tarea de contrato de escritura. Fuera también: síntesis de código de aplicación. En specIR, estas operaciones solo se exponen como tools MCP; no se implementan funciones propias de CRUD ni escrituras directas al filesystem o a índices SLDB. La creación, edición, borrado, validación de modelos, reglas e integridad se delegan en las operaciones existentes de `sldb.api`; si una capacidad falta, se pide extensión al desk SLDB.

## Implementation Path

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

Las tools envuelven las operaciones de escritura, prevalidación, reglas y transiciones que la matriz de auditoría marca como existentes en la API pública de SLDB; lo que falte se resuelve en SLDB, no en specIR. Delegación obligatoria por operación: crear documento con `sldb.api.create_document`; editar payload de documento existente con `sldb.api.save_document_payload`; borrar con `sldb.api.delete_document`. RelationDoc, RelationTypeDoc y RuleDoc se escriben como documentos mediante esas mismas funciones con su modelo registrado, no mediante mutación propia del índice de aristas. Los tools MCP convierten argumentos tipados a llamadas API y devuelven sus resultados/errores; no duplican serialización, renderizado, validación de modelo/reglas, mantenimiento de índices, ni borrado de archivos. Para agrupar cambios usa `sldb.api.transaction` cuando corresponda. La ejecución en seco y el contrato de precondición usan mecanismos existentes de SLDB; si la API pública no los ofrece, el nodo no crea una implementación paralela en specIR y deja la brecha solicitada a SLDB.

## Validation

_List the checks required before this task can close._

- Una ejecución en seco devuelve lo que se escribiría y no cambia ningún archivo del store.
- Aplicar un cambio validado sobre un store que cambió después de la validación es rechazado con un error que lo dice.
- Una arista que viola los tipos de origen o destino, la cardinalidad o la condición de su RelationTypeDoc es rechazada antes de escribir.
- Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad de la regla, y la respuesta nombra la regla.
- Ninguna tool de escritura recibe texto libre para interpretar: solo argumentos tipados.
- Cada documento escrito lleva en su procedencia quién y por qué operación se escribió.
- Una tool por encima del nivel de escritura permitido responde error sin evaluar nada.
- No existe ninguna tool que cree o modifique módulos Python.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan contra un store de prueba y un agente completa el ciclo proponer, validar y aplicar sobre un documento y sobre una arista.

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
Cold-bundle de la tarea task-ir04-escritura-validada-por-mcp-proponer-validar-aplicar: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Una ejecución en seco devuelve lo que se escribiría y no cambia ningún archivo del store.
- Aplicar un cambio validado sobre un store que cambió después de la validación es rechazado con un error que lo dice.
- Una arista que viola los tipos de origen o destino, la cardinalidad o la condición de su RelationTypeDoc es rechazada antes de escribir.
- Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad de la regla, y la respuesta nombra la regla.
- Ninguna tool de escritura recibe texto libre para interpretar: solo argumentos tipados.
- Cada documento escrito lleva en su procedencia quién y por qué operación se escribió.
- Una tool por encima del nivel de escritura permitido responde error sin evaluar nada.
- No existe ninguna tool que cree o modifique módulos Python.

