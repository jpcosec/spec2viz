FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T03:55:40Z'
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

Auditar estas capacidades con una necesidad acotada: (1) listar/describir modelos y tipos de relación: enumerar modelos y sus campos; (2) leer docs/campos: resolver por la identidad canónica de documento que SLDB ya documente y devolver datos; no inventar otro formato de dirección, y si SLDB no lo define registrar brecha; (3) vecinos/recorridos: seguir aristas entrantes/salientes por profundidad acotada; (4) búsqueda por predicados: buscar documentos por filtros de campo que soporte la API pública existente, sin exigir un lenguaje nuevo; (5) resolver vistas: evaluar una ViewDoc almacenada y devolver el resultado según contrato SLDB, sin fijar formato propio; (6) crear/editar/borrar docs y aristas y escribir RelationTypeDoc/RuleDoc con validación; (7) registrar clases de modelos por código; (8) comprobar integridad; (9) consultar historia/procedencia; (10) detectar una revisión/estado de store utilizable como precondición contra escrituras obsoletas; (11) revertir una escritura aplicada si la API lo permite. Cada fila usa campos fijos: capacidad; necesidad (una frase que explica actor, entrada y resultado requerido, sin diseñar interfaz MCP); estado; evidencia; brecha; acción; referencia de handoff. Estados exactos: disponible (una operación pública cubre la necesidad), requiere-extensión-en-SLDB (hay operaciones públicas relacionadas, pero su composición no puede cumplirla) y faltante (no se encuentra operación pública relacionada en el inventario revisado). Si se cubre con varias operaciones, disponible y acción=componer. Las acciones exactas son usar, componer o solicitar-extensión; disponible usa usar/componer y ambos estados no disponibles usan solicitar-extensión y requieren aparecer en la nota agregada. Citar rutas existentes bajo sldb/src/sldb/api/ y símbolos públicos para disponible; si es composición, citar cada símbolo. Los otros estados enumeran módulos existentes revisados y explican por qué no alcanzan; nunca citan rutas inexistentes. Listar los módulos API y documentos de arquitectura revisados para que la ausencia sea comprobable. Leer pron/source/spec/14-superficie-mcp.md está permitido solo como referencia documental para identificar contratos; no ejecutar ni importar pron, ni usar sus módulos. Si hay alguna fila no disponible, enviar una única nota agregada al desk de SLDB; registrar el ID en la sección Resumen del informe y en cada fila afectada. Si ninguna fila requiere extensión/falta, el Resumen declara que no se envió nota. Fuera: escribir código, modificar SLDB, diseñar tools, usar pron directamente o decidir el contrato final de escritura.

## Implementation Path

_Outline the expected implementation route or affected surface._

Documento de auditoría dentro del repo de specIR. Lectura de sldb/src/sldb/api/ y de la documentación de arquitectura de SLDB; como referencia de contrato, pron/source/spec/14-superficie-mcp.md. Solo si una fila queda como faltante real (no existe ni se puede componer con operaciones públicas existentes), se envía una nota al desk de SLDB con deskops message send; si no hay faltantes, no se envía nada.

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

