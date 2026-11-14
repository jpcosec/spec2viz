---
sldb:
  by: agent
  at: '2026-11-12T01:25:34Z'
  authority: generated
  via: save_document_payload
id: task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:procedencia
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp
pills:
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/decisiones/procedencia-y-divergencia.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
from_drawer: desk/drawer/tasks/task-ir05-decisi-n-procedencia-y-divergencia-entre-c-digo-y-modelo.md
---

# IR05 Decisión: procedencia y divergencia entre código y modelo

## Rationale

_Explain why this task exists or the business driver behind it._

Hoy hay tres listas distintas para decir cuánto se confía en un nodo o relación, y ninguna regla sobre qué pasa cuando el código fuente cambia. Sin una sola taxonomía, una inferencia puede terminar tratada como hecho.

## Goal

_Describe the concrete result this task must produce._

Una taxonomía canónica de procedencia para specIR y una regla para la divergencia entre el modelo y el código del que se extrajo.

## Scope

_State what is in scope and what is out of scope._

Dentro: elegir la taxonomía canónica entre (1) observado, inferido, validado (fundamentos_modelado_semantico_mcp.md, sección 7); (2) observado, derivado estáticamente, inferencia de LLM, verificado (Plan_IR.md, fase 5); (3) la autoridad de SLDB: source_raw, authored, theorem, generated, cache (sldb/src/sldb/models/provenance.py); definir las equivalencias; decidir si la relación entre un nodo extraído y su fuente se expresa con las anclas de código de SLDB; decidir qué prevalece cuando modelo y código discrepan y cómo se representa lo desconocido. Fuera: implementar extractores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Cada decisión se registra como atom. Lectura de sldb/docs/architecture/provenance.md y anchoring.md.

## Validation

_List the checks required before this task can close._

- Existe un atom con la taxonomía canónica y la tabla de equivalencias con las otras dos listas.
- Existe un atom que dice cómo se representa lo desconocido y cómo una inferencia pasa a validada, y por acción de quién.
- Existe un atom sobre divergencia: qué ocurre con un nodo cuya fuente cambió.
- Si la decisión exige algo que SLDB no tiene, la carencia está identificada con la fila correspondiente de la matriz de auditoría.

## Done When

_Name the observable condition that makes the task complete._

Los tres atoms existen y las tareas de tipos de dominio y de extractores pueden citar una sola taxonomía.
