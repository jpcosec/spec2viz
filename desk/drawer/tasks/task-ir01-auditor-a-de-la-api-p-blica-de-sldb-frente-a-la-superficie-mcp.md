---
id: task-ir01-auditor-a-de-la-api-p-blica-de-sldb-frente-a-la-superficie-mcp
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
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-specir-no-depende-de-pron-adopta-contratos-no-código
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

Dentro: una fila por capacidad de la superficie MCP: listar y describir modelos y tipos de relación; leer documento y campo; vecinos y recorrido del grafo; búsqueda por predicados; resolver una vista; escritura validada de documentos y aristas; reglas (RuleDoc) y transiciones; creación y edición de modelos; integridad; historia; identificador de estado del store utilizable como precondición de escritura; forma de deshacer una escritura. Fuera: escribir código, modificar SLDB, diseñar las tools.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.docs (se asigna al autorar la tarea activa con deskops add task --task-type; en una candidata el campo task_type no es editable). Documento de auditoría dentro del repo de specIR. Lectura de sldb/src/sldb/api/ y de la documentación de arquitectura de SLDB; como referencia de contrato, pron/source/spec/14-superficie-mcp.md. Solo si una fila queda como faltante real (no existe ni se puede componer con operaciones públicas existentes), se envía una nota al desk de SLDB con deskops message send; si no hay faltantes, no se envía nada.

## Validation

_List the checks required before this task can close._

- Cada fila de la matriz cita una ruta existente bajo sldb/src/sldb/api/ o declara explícitamente que la capacidad falta.
- Ninguna fila se apoya en sldb.store, sldb.core ni en pron.
- La matriz responde explícitamente si existe un identificador de estado del store y si existe una forma de deshacer una escritura.
- Por cada fila marcada como faltante real existe una nota enviada al desk de SLDB; si no hay faltantes, el documento lo dice y no hay nota.

## Done When

_Name the observable condition that makes the task complete._

La matriz está escrita, cada fila tiene estado y cita, y los faltantes reales (si los hay) están notificados a SLDB.
