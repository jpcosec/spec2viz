FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T03:53:05Z'
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

Auditar estas capacidades con una necesidad acotada: (1) listar/describir modelos y tipos de relación: enumerar modelos y sus campos; (2) leer docs/campos: resolver una dirección estable y devolver datos; (3) vecinos/recorridos: seguir aristas entrantes/salientes por profundidad acotada; (4) búsqueda por predicados: buscar documentos por los filtros de campo que soporte la API pública existente, sin exigir un lenguaje nuevo; (5) resolver vistas: evaluar una ViewDoc almacenada y devolver el resultado según contrato SLDB; (6) crear/editar/borrar docs y aristas y escribir RelationTypeDoc/RuleDoc con validación; (7) registrar clases de modelos por código; (8) comprobar integridad; (9) consultar historia/procedencia; (10) detectar una revisión/estado de store utilizable como precondición contra escrituras obsoletas; (11) revertir una escritura aplicada si la API lo permite. Cada fila usa campos fijos: capacidad; necesidad (una frase que explica actor, entrada y resultado requerido, sin diseñar interfaz MCP); estado; evidencia; brecha; acción; referencia de handoff. Estados exactos: disponible (una operación pública cubre la necesidad), requiere-extensión-en-SLDB (hay operaciones públicas relacionadas, pero su composición no puede cumplirla) y faltante (no se encuentra operación pública relacionada en el inventario revisado). Si se cubre con varias operaciones, disponible y acción=componer. Las acciones exactas son usar, componer, solicitar-extensión o ninguna; disponible usa usar/componer, los otros estados usan solicitar-extensión salvo que la necesidad dependa de una decisión pendiente del dueño, en cuyo caso ninguna y se explica. Disponible cita rutas existentes bajo sldb/src/sldb/api/ y símbolo(s) públicos. Los otros estados enumeran módulos existentes revisados y explican por qué no alcanzan; nunca citan rutas inexistentes. El informe lista los módulos API y documentos de arquitectura revisados para que la ausencia sea comprobable. Agrupar todos los faltantes/extensiones en una sola nota al desk de SLDB y guardar el ID en el resumen y las filas afectadas; si no hay faltantes, declarar que no se envió nota. Fuera: escribir código, modificar SLDB, diseñar tools, usar pron directamente, o decidir el contrato final de escritura.

## Implementation Path

_Outline the expected implementation route or affected surface._

Documento de auditoría dentro del repo de specIR. Lectura de sldb/src/sldb/api/ y de la documentación de arquitectura de SLDB; como referencia de contrato, pron/source/spec/14-superficie-mcp.md. Solo si una fila queda como faltante real (no existe ni se puede componer con operaciones públicas existentes), se envía una nota al desk de SLDB con deskops message send; si no hay faltantes, no se envía nada.

## Validation

_List the checks required before this task can close._

- Cada una de las once capacidades del scope tiene exactamente una fila con los campos fijos y necesidad de una frase con actor/entrada/resultado. - Cada fila usa exactamente uno de los tres estados cerrados y una acción permitida; las combinaciones estado/acción cumplen scope. - Una capacidad disponible cita una o más rutas existentes en sldb/src/sldb/api/ y los símbolos públicos; una composición nombra todos los símbolos. - Una capacidad requiere-extensión-en-SLDB o faltante lista los módulos existentes inspeccionados y describe la insuficiencia sin inventar símbolos/rutas. - El informe lista las fuentes revisadas y no depende de sldb.store, sldb.core ni de pron. - Si alguna fila requiere extensión, se envía una única nota agregada al desk de SLDB y su ID aparece en resumen y filas afectadas; si no hay faltantes, se declara que no se envió nota.

## Done When

_Name the observable condition that makes the task complete._

La matriz está escrita, cada fila tiene estado y cita, y los faltantes reales (si los hay) están notificados a SLDB.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

