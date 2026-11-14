FILE:desk/tasks/task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:15Z'
  authority: generated
  via: save_document_payload
id: task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
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
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- pyproject.toml
- src/specir/__init__.py
- src/specir/mcp/__init__.py
- src/specir/mcp/server.py
- src/specir/mcp/read_tools.py
- src/specir/mcp/addresses.py
- src/specir/mcp/paging.py
- tests/conftest.py
- tests/mcp/test_read_tools.py
- tests/mcp/test_no_writes.py
- tests/test_imports.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
from_drawer: desk/drawer/tasks/task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real.md
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

Paquete Python specIR con dependencia en structuredLanguageDB y el SDK de MCP como extra opcional; las tools son envoltorios de las operaciones que la matriz de auditoría marca como existentes.

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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

