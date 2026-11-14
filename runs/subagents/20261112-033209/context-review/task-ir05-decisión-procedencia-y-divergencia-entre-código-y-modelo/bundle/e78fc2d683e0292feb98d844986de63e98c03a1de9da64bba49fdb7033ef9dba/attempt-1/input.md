FILE:desk/tasks/task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo.md
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

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

FILE:desk/atoms/atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir.md
---
sldb:
  by: agent
  at: '2026-11-12T00:48:16Z'
  authority: generated
  via: save_document_payload
id: atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
title: Principios de seguridad de la superficie MCP de specIR
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- topic:procedencia
- layer:superficie
provenance: fundamentos_modelado_semantico_mcp.md
---

# Principios de seguridad de la superficie MCP de specIR

## Answer

La superficie MCP sigue estos principios: las consultas no tienen efectos laterales; proponer, validar y aplicar una modificación son pasos separados; no se aplica un cambio sobre un estado que ya no es el que se validó; cada nodo y relación declara su procedencia y una inferencia de un LLM nunca pasa a hecho validado en silencio; los límites de escritura los impone el servidor, no el agente ni la interfaz; el sistema conserva lo que desconoce en vez de rellenarlo. Son principios, no mecanismos: cómo se representa una propuesta, qué precondición protege la aplicación, dónde se declara el nivel de escritura permitido y qué taxonomía de procedencia se usa están pendientes de decisión en las candidatas de contrato de escritura y de procedencia.

FILE:instruccion
Cold-bundle de la tarea task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Existe un atom con la taxonomía canónica y la tabla de equivalencias con las otras dos listas.
- Existe un atom que dice cómo se representa lo desconocido y cómo una inferencia pasa a validada, y por acción de quién.
- Existe un atom sobre divergencia: qué ocurre con un nodo cuya fuente cambió.
- Si la decisión exige algo que SLDB no tiene, la carencia está identificada con la fila correspondiente de la matriz de auditoría.

