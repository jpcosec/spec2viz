FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T04:00:09Z'
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

Matriz para el cliente MCP de specIR, con el agente conectado como actor. Auditar exactamente estas necesidades: (1) catálogo de modelos y tipos de relación, con campos/tipos; (2) leer payload por identidad estable Model:name y campo; (3) vecinos y recorrido dirigido de aristas con profundidad; (4) buscar documentos por filtros de campo en la sintaxis existente de sldb.api.where/search, sin pedir filtros que SLDB no documenta; (5) ejecutar una ViewDoc existente y obtener su resultado; (6) crear, editar y borrar documentos y RelationDoc/RelationTypeDoc/RuleDoc con las validaciones del modelo/reglas; (7) registrar modelos Python ya definidos por código; (8) revisar integridad del store e índice de aristas; (9) consultar journal e historial de documento con procedencia; (10) lectura de una huella/estado del store y aplicación de escritura que la compare atómicamente, rechazando el cambio si el estado esperado ya no coincide; (11) revertir un cambio ya confirmado con efecto persistente y registro durable, como exige pron kb_undo. No considerar disponible una capacidad de concurrencia si solo se puede comparar en el llamador antes de escribir y la operación no rechaza estado obsoleto atómicamente. Actor para toda fila: agente MCP de specIR. La necesidad es la conducta requerida; no define nombre, firma o formato de una futura tool. Identidad Model:name es el nombre estable que SLDB registra al crear/trackear un doc; citar sldb://document/Model:name cuando la documentación la respalde y el argumento exacto que aceptan las operaciones. El resultado de vistas usa el contrato público existente, no un formato inventado. Los filtros son solo los predicados que ya define SLDB; documentar si la búsqueda pública exige además texto libre. Evaluar estado=disponible solo si las operaciones públicas ofrecen exactamente la conducta requerida, directamente o como composición documentada; si hay API relacionada pero falta un comportamiento, requiere-extensión-en-SLDB; si no existe operación relacionada, faltante. Acciones exactas: usar/componer para disponible; solicitar-extensión para ambos estados no disponibles. Toda fila disponible lleva referencia de handoff —; cada fila no disponible lleva sldb:<note-id>, misma nota agregada. El informe tiene sección Markdown # Resumen donde se consigna ese ID o que no se envió nota. Se inspecciona todo archivo Python recursivamente bajo ../sldb/src/sldb/api/ y los documentos enumerados en Implementation Path. La ausencia se justifica contra ese corpus exacto. Leer ../pron/source/spec/14-superficie-mcp.md se permite solo como referencia documental; no importar/ejecutar pron, ni leer código fuera de sldb.api. Fuera: diseñar tools, escribir código, editar otros repos y decidir el contrato de escritura.

## Implementation Path

_Outline the expected implementation route or affected surface._

Trabajar desde la raíz /home/jp/proyectos/SLDB_1/IR; todas las rutas relativas parten de ahí. Escribir solo docs/auditoria/sldb-api-frente-a-mcp.md (crear docs/auditoria si hace falta). Inspeccionar recursivamente cada .py bajo ../sldb/src/sldb/api/ (incluidos todos sus subpaquetes), ../sldb/docs/README.md, ../sldb/docs/addressability_model.md y los documentos ../sldb/docs/architecture/current-system-overview.md, derived-store-boundary.md, edges.md, journal-authority.md, model-authoring.md, model-federation-on-the-graph.md, notations-and-views.md, provenance.md, rules.md, rules-language.md y selectors.md. Leer ../pron/source/spec/14-superficie-mcp.md como único documento externo de referencia sobre el contrato MCP; no leer código de pron. Por cada fila no disponible, agregar al único mensaje a sldb: capacidad y necesidad requerida; símbolos/rutas públicas revisadas; comportamiento que falta; contrato público sugerido como pregunta al equipo propietario, no como decisión; referencia a TaskDoc IR01. Usar deskops message send --to sldb desde la raíz de este repo. Si cualquier fila es requiere-extensión-en-SLDB o faltante, la nota se envía una sola vez; copiar el ID devuelto como sldb:<id> al Resumen del informe y filas afectadas. Si ninguna es no disponible, poner — en todas las referencias y declarar en # Resumen que no se envió nota. No leer módulos internos de SLDB ni importar/ejecutar pron.

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

