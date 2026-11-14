---
id: task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
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
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
---

# IR03 Servidor MCP de solo lectura sobre un store SLDB real

## Rationale

_Explain why this task exists or the business driver behind it._

El primer hito del proyecto es que un agente explore un store SLDB real por MCP. La lectura no necesita esperar las decisiones de escritura.

## Goal

_Describe the concrete result this task must produce._

Un servidor MCP de solo lectura, en el paquete specIR, con el que un agente descubre modelos, lee documentos, recorre relaciones y resuelve vistas de un store SLDB.

## Scope

_State what is in scope and what is out of scope._

Dentro: servidor MCP por stdio sobre la API pública de SLDB con tools para listar y describir modelos y tipos de relación, leer un documento o un campo, vecinos y recorrido por relación, búsqueda por predicados, resolver una vista (ViewDoc o SpecDoc) a JSON, e integridad del store. Fuera: cualquier escritura, tipos de dominio nuevos, extractores, renderizado de diagramas.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.code (se asigna al autorar la tarea activa; task_type no es editable en una candidata). Paquete Python specIR con dependencia en structuredLanguageDB y el SDK de MCP como extra opcional; las tools son envoltorios de las operaciones que la matriz de auditoría marca como existentes.

## Validation

_List the checks required before this task can close._

- Pruebas con un cliente MCP contra un store de prueba: cada tool devuelve JSON estructurado y, por cada documento, su dirección estable.
- Todo conjunto llega paginado, con su total y una marca cuando quedó cortado.
- Montar el store y ejecutar todas las tools de lectura no modifica ningún archivo del store (comparación del árbol antes y después).
- Una consulta sobre algo que el store no declara devuelve conjunto vacío con explicación, no un error opaco.
- Una prueba de imports comprueba que el paquete no importa pron, spec2viz, ni módulos de SLDB fuera de sldb.api.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y un agente conectado al servidor recorre un store real sin escribir en él.
