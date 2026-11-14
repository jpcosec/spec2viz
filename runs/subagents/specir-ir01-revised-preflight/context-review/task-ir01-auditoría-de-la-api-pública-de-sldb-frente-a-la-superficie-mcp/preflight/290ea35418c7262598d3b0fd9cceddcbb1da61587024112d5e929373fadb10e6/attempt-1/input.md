FILE:desk/tasks/task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp.md
---
sldb:
  by: agent
  at: '2026-11-12T03:51:29Z'
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

Dentro: una fila por capacidad necesaria para la superficie MCP de specIR: listar/describir modelos y tipos de relación; leer documentos y campos; vecinos y recorridos; búsqueda por predicados; resolver vistas; escritura validada de documentos, aristas, RelationTypeDoc y RuleDoc; creación/edición de modelos; integridad; historia; precondición/versionado del store; deshacer. Cada fila incluye capacidad, necesidad, estado, evidencia, brecha y acción. Estados cerrados: disponible (API pública suficiente, incluso si se compone de varias operaciones), requiere-extensión-en-SLDB (hay API pública relacionada pero no compone el contrato requerido) y faltante (no hay operación pública encontrada tras revisar las fuentes declaradas). Para disponible, citar ruta bajo sldb/src/sldb/api/ y símbolo público; si es composición, citar cada símbolo. Para requiere-extensión-en-SLDB o faltante, citar las fuentes y rutas inspeccionadas y explicar por qué no alcanza; no inventar una función pública. La evidencia de ausencia es el inventario de fuentes revisadas, no una ruta inexistente. Si hay faltante real, enviar una sola nota al desk de SLDB y registrar su ID en la fila correspondiente del informe. Fuera: código, cambios en SLDB, diseño de tools y uso directo de pron.

## Implementation Path

_Outline the expected implementation route or affected surface._

Documento de auditoría dentro del repo de specIR. Lectura de sldb/src/sldb/api/ y de la documentación de arquitectura de SLDB; como referencia de contrato, pron/source/spec/14-superficie-mcp.md. Solo si una fila queda como faltante real (no existe ni se puede componer con operaciones públicas existentes), se envía una nota al desk de SLDB con deskops message send; si no hay faltantes, no se envía nada.

## Validation

_List the checks required before this task can close._

- El informe cubre todas las capacidades enumeradas en scope con los campos capacidad, necesidad, estado, evidencia, brecha y acción. - Cada fila usa exactamente uno de los tres estados definidos en scope. - Toda fila disponible cita una o más rutas existentes en sldb/src/sldb/api/ y los símbolos públicos que satisfacen la capacidad. - Toda fila requiere-extensión-en-SLDB o faltante documenta las fuentes existentes revisadas y la brecha; ninguna cita rutas inventadas. - Una composición declara todos los símbolos públicos utilizados. - Si existe un faltante real, el informe incluye el ID de la nota enviada al desk de SLDB; si no, declara que no se envió nota. - Ninguna fila depende de sldb.store, sldb.core ni de pron.

## Done When

_Name the observable condition that makes the task complete._

La matriz está escrita, cada fila tiene estado y cita, y los faltantes reales (si los hay) están notificados a SLDB.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

