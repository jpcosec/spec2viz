---
sldb:
  by: agent
  at: '2026-11-15T05:03:22Z'
  authority: generated
  via: save_document_payload
id: task-ir02-decisión-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:mcp
current_node: ritual-testing
history:
- task_activates
references:
- docs/decisiones/contrato-de-escritura-mcp.md
- atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado
- atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2
- atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor
- atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
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
