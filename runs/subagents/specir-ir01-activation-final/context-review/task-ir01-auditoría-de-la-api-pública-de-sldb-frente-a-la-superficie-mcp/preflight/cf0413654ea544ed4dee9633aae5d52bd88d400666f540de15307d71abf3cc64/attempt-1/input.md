FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T03:56:49Z'
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

Auditar once capacidades: listar modelos/campos/tipos de relación; leer documento por la identidad canónica ya documentada por SLDB; vecinos/recorridos acotados; búsqueda por filtros ya soportados; resolver ViewDoc con el contrato SLDB existente; escrituras validadas de documentos, aristas, RelationTypeDoc y RuleDoc; registrar clases de modelos; integridad; historia/procedencia; detectar estado para rechazar escritura obsoleta; revertir una escritura si existe operación pública. Necesidad se redacta como una frase con actor, entrada y resultado, sin diseñar una tool MCP. Si SLDB no documenta identidad estable o una semántica necesaria, registrarla como brecha, sin inventar contrato. Estados exactos: disponible (una operación pública cubre la necesidad), requiere-extensión-en-SLDB (hay operaciones relacionadas pero no una composición suficiente) y faltante (no se encuentra operación relacionada). Acciones: usar/componer para disponible; solicitar-extensión para ambos estados no disponibles. La referencia de handoff es — para toda fila disponible y sldb:<id> para cada fila no disponible, todas referidas a la nota agregada única; el Resumen está en la sección Markdown # Resumen del informe. Fuentes API inspeccionadas: todos los módulos de ../sldb/src/sldb/api/; documentos de arquitectura a revisar están enumerados en Implementation Path. La spec de pron se puede leer solo como referencia documental: no importar ni ejecutar pron, ni abrir módulos internos de SLDB. Fuera: implementar código, cambiar SLDB o diseñar tools.

## Implementation Path

_Outline the expected implementation route or affected surface._

Crear solo docs/auditoria/sldb-api-frente-a-mcp.md. Inspeccionar todos los módulos bajo ../sldb/src/sldb/api/ y estos documentos del repo SLDB: docs/README.md, docs/addressability_model.md, docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md y selectors.md. Leer ../pron/source/spec/14-superficie-mcp.md solo como referencia documental permitida. Si al menos una capacidad tiene estado requiere-extensión-en-SLDB o faltante, enviar una sola nota agregada con deskops message send --to sldb; registrar su ID como sldb:<id> en el Resumen del informe y en filas afectadas. Si todas están disponibles, usar el literal — en referencia de handoff y declarar en Resumen que no se envió nota. En el informe el Resumen es la sección Markdown # Resumen, no el campo summary del TaskDoc. Para otras filas disponibles, referencia de handoff también es —. No abrir/importar módulos internos de SLDB ni ejecutar código de pron.

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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

