FILE:desk/tasks/task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real.md
---
sldb:
  by: agent
  at: '2026-11-12T04:47:11Z'
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

Dentro: servidor MCP por stdio sobre la API pública de SLDB con tools para listar y describir modelos y tipos de relación, leer un documento o campo, consultar vecinos salientes/entrantes filtrados por tipo de relación y obtener la vecindad a profundidad por dirección, buscar por predicados, resolver una vista (ViewDoc o SpecDoc) a JSON e inspeccionar integridad del store. Las tools de grafo son adaptadores MCP delgados. La vecindad multi-salto recorre los tipos de relación del índice según la dirección; el contrato no promete filtrar un tipo específico en cada salto. specIR no mantiene índice de aristas, algoritmo de recorrido, parser de predicados ni backend de grafo propio. Fuera: paths entre dos extremos (graph_path/graph_paths), cualquier escritura, tipos de dominio nuevos, extractores y renderizado de diagramas.

## Implementation Path

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

Paquete Python specIR con dependencia en structuredLanguageDB y el SDK de MCP como extra opcional; las tools son envoltorios de las operaciones que la matriz de auditoría marca como existentes. Store de las pruebas: una copia aislada del store real de este repo, sin registros fabricados. La obtiene un fixture de tests/conftest.py que copia a un directorio temporal de la prueba las carpetas .sldb/, sldb/ y desk/ de la raíz del repo (los documentos reales del desk: atoms, tareas, rituales, reglas y tipos de relación), sin copiar .sldb_cache/. Sobre la copia solo operan herramientas públicas de SLDB: sldb stores update para reconstruir los índices derivados, sldb edges rebuild para el índice de aristas y sldb stores check para comprobar la integridad antes de usarla; el store federado deskops, que el original enlaza por ruta relativa, se vuelve a enlazar en la copia con sldb stores add apuntando a su ruta real, y con el mismo comando se enlaza además el store real de spec2viz (../spec2viz/.sldb respecto de la raíz de este repo); ambos se leen en sitio en solo lectura y las pruebas no escriben en ellos. El servidor bajo prueba es el servidor MCP real, lanzado por stdio y consultado con el cliente del SDK de MCP: no se simulan ni la API de SLDB, ni el servidor, ni el cliente. La prueba de resolución de vistas usa el SpecDoc real class.sldb-models del store federado de spec2viz: primero comprueba que ese documento resuelve desde la federación de la copia y después lo lee y resuelve su vista por las tools del servidor. Si el store de spec2viz o ese documento dejan de existir, la prueba falla con un mensaje que nombra el store y el documento que faltan; no se sustituye por un documento inventado. Mapeo exacto: vecinos salientes/entrantes con filtro de tipo usan `sldb.api.edges_from`/`edges_to`; vecindad multi-salto con dirección y profundidad usa `sldb.api.graph.collect_neighborhood_by_direction`, que recorre las relaciones del índice y no filtra un tipo en cada salto. Esta tarea no expone paths entre dos extremos; si se requieren más adelante, son otra tool delgada que delega en `graph_path` (una ruta, con `directed`) o `graph_paths` (varias rutas, con `relations` y `cutoff`). specIR no implementa ni itera un recorrido propio como fallback.

## Validation

_List the checks required before this task can close._

- Las pruebas corren con un cliente MCP real contra el servidor real lanzado por stdio sobre la copia aislada del store de este repo; cada tool devuelve JSON estructurado y, por cada documento, su dirección estable.
- Los documentos que devuelven las tools existen en el store original con el mismo id y contenido (comparación contra los archivos de desk/ del repo).
- Todo conjunto llega paginado, con su total y una marca cuando quedó cortado; se prueba sobre el modelo con más documentos del store.
- El SpecDoc real class.sldb-models del store de spec2viz resuelve desde la federación de la copia, y las tools de lectura y de resolución de vistas lo devuelven con el mismo contenido que tiene en ../spec2viz/.sldb; si el store o el documento faltan, la prueba falla nombrando cuál falta.
- Montar la copia y ejecutar todas las tools de lectura no modifica ningún archivo de la copia ni de los stores federados de deskops y de spec2viz (comparación del árbol antes y después).
- El store original del repo no cambia durante las pruebas (comparación del árbol de .sldb/ y desk/ antes y después).
- Una consulta sobre algo que el store no declara devuelve conjunto vacío con explicación, no un error opaco.
- Una prueba de imports comprueba que el paquete no importa pron, spec2viz, ni módulos de SLDB fuera de sldb.api.
- Ninguna prueba crea documentos de contenido inventado ni sustituye la API de SLDB, el servidor o el cliente por un doble.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan sobre la copia aislada del store real de este repo y un agente conectado al servidor recorre ese store sin escribir en él.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

