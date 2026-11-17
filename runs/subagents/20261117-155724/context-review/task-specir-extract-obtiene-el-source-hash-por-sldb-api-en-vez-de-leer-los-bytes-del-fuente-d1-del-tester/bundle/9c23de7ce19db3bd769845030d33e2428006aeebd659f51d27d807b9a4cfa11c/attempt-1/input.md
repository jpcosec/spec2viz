FILE:desk/tasks/task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester.md
---
sldb:
  by: agent
  at: '2026-11-17T14:06:54Z'
  authority: generated
  via: create_document
id: task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir08-extractor-estático-django-drf-y-sql
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# specir.extract obtiene el source_hash por sldb.api en vez de leer los bytes del fuente (D1 del tester de IR08)

## Rationale

_Explain why this task exists or the business driver behind it._

El tester deskops-t-05230b7b7270-a2 de IR08 encontró que src/specir/extract/write.py, en checked_blocks, lee los bytes del archivo fuente (read_bytes) para recalcular el source_hash y compararlo con el del fact. No interpreta código, pero contradice el guardrail de que specIR solo usa la API pública de sldb y no lee fuentes. IR08 se cerró aceptando la excepción por decisión del coordinador, con esta tarea como seguimiento.

## Goal

_Describe the concrete result this task must produce._

Que specir.extract compruebe que el ancla corresponde al fact sin leer ningún archivo fuente: el source_hash sale de sldb.api (por ejemplo, un code_facts de la ruta justo antes de escribir, comparado con el fact del plan), o se pide a sldb que record_anchor lo devuelva.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/specir/extract/write.py (checked_blocks) y una prueba en tests/extract/ que falle si el extractor abre o lee un archivo fuente del fixture (por ejemplo, vigilando open y Path.read_bytes durante la extracción). Fuera: cualquier otro cambio del extractor. Si hace falta un dato que sldb.api no da, se pide por el desk de sldb y la tarea se detiene.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sustituir la línea que hace hashlib.sha256 sobre (root / fact[path]).read_bytes() por una comprobación hecha con sldb.api.code.code_facts (el source_hash del fact recién leído para esa ruta debe coincidir con el del plan), manteniendo el ValueError con el ref si no coinciden y la regla de no escribir nada si una ancla falla.

## Validation

_List the checks required before this task can close._

- grep -rnE 'read_bytes|read_text|open\(' src/specir/extract no devuelve nada.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/extract tests/models/test_blog_chain.py sale con rc 0, con la prueba nueva que vigila las lecturas de archivo.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

src/specir/extract no contiene read_bytes, read_text ni open sobre fuentes, y las pruebas de tests/extract siguen verdes.

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

FILE:instruccion
Cold-bundle de la tarea task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -rnE 'read_bytes|read_text|open\(' src/specir/extract no devuelve nada.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/extract tests/models/test_blog_chain.py sale con rc 0, con la prueba nueva que vigila las lecturas de archivo.
- deskops graph missing --root . sale con rc 0.

