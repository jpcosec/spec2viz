---
id: task-ir02-decisi-n-contrato-de-escritura-y-nivel-de-mutabilidad-del-mcp
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:mcp
current_node: ''
history: []
references: []
depends_on:
- task-ir01-auditor-a-de-la-api-p-blica-de-sldb-frente-a-la-superficie-mcp
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
---

# IR02 Decisión: contrato de escritura y nivel de mutabilidad del MCP

## Rationale

_Explain why this task exists or the business driver behind it._

La superficie MCP promete proponer, validar y aplicar como pasos separados, pero no está decidido con qué mecanismo ni quién limita hasta dónde puede escribir un agente. Sin esa decisión la escritura por MCP no se puede diseñar.

## Goal

_Describe the concrete result this task must produce._

Cuatro decisiones registradas: qué es una propuesta de cambio, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido, y si existe deshacer.

## Scope

_State what is in scope and what is out of scope._

Dentro: (a) propuesta de cambio como lote prevalidado sin persistir o como documento persistente; (b) precondición que impide aplicar sobre un store que cambió desde la validación; (c) dónde se declara el nivel de escritura permitido (contenido, reglas y tipos de relación, modelos): al arrancar el servidor, en un documento del store, o por actor; (d) si hay una operación de deshacer o basta la historia en git. Fuera: implementar; decidir permisos multiusuario.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.decision (se asigna al autorar la tarea activa; task_type no es editable en una candidata). Cada decisión se registra como atom con deskops add atom y parte de la matriz de la candidata de auditoría de la API de SLDB.

## Validation

_List the checks required before this task can close._

- Existe un atom por cada una de las cuatro decisiones, y cada uno nombra la alternativa descartada y su motivo.
- Cada decisión nombra la operación de la API pública de SLDB que la sostiene según la matriz de auditoría, o la carencia notificada a SLDB.
- Ninguna decisión introduce un camino de escritura al store que no pase por la API pública de SLDB.
- El atom de reglas de seguridad de la superficie MCP queda actualizado o complementado con el mecanismo decidido.

## Done When

_Name the observable condition that makes the task complete._

Los cuatro atoms existen y la candidata de escritura por MCP puede citar un mecanismo concreto para cada regla.
