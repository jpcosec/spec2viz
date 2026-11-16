FILE:desk/tasks/task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4.md
---
sldb:
  by: agent
  at: '2026-11-16T21:45:36Z'
  authority: generated
  via: save_document_payload
id: task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
- task-espejo-deskops-deskops-sldb-deja-de-enlazar-el-store-de-spec2viz-g5-opción-b
depends_on:
- task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/spec2viz/acta-de-retiro.md
- docs/spec2viz/matriz-de-cobertura.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR13h Registrar en el acta que deskops ya no depende de spec2viz y actualizar G4

## Rationale

_Explain why this task exists or the business driver behind it._

El coordinador de deskops avisó el 2026-11-16 que deskops quedó migrado de spec2viz a specir, con todo en origin main de deskops (ee9bc3cd). Commits: el enlace al store de spec2viz (421d6a27, closeout 74ffdb63), la regla de desk_graph.py:75 (42b752ea, closeout b716bf85) y las skills y el script render_diagram.py (ce66f69e, closeout 2421ca29). La corrida del comprobador del 2026-11-16 a las 18:50 da 0 dependencias de deskops, 63 en total y 9 filas no acreditadas. El acta todavía registra a deskops con 22 dependencias. La línea de G4 de la matriz sigue nombrando a graph_ui, deskops y pron como consumidores con dependencias, y lo señalaron IR13g y su tester.

## Goal

_Describe the concrete result this task must produce._

El acta registra a deskops como resuelto, con sus commits, y trae una corrida nueva del comprobador. La línea de G4 de la matriz refleja los consumidores que de verdad quedan.

## Scope

_State what is in scope and what is out of scope._

Dentro: docs/spec2viz/acta-de-retiro.md y docs/spec2viz/matriz-de-cobertura.md. (1) En el acta, en la tabla Consumidores, la fila de deskops pasa a resuelto en la columna Cambio que lo resolvió, citando los tres pares de commits y que están en origin; su columna Dependencias sigue el precedente de pron y graph_ui. (2) La fila G4 del gate y el punto de Consumidores de Lo que falta dejan de nombrar a deskops como pendiente. Lo que queda en G4 es IR (los oráculos de paridad en pruebas, que se retiran al declarar), sldb (runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5) y spec2viz/.sldb (G5). (3) Una corrida nueva de specir retirement check con las 5 rutas, en un bloque fechado con el formato del bloque de IR13g. (4) En la matriz, solo la línea de estado de G4: que diga los consumidores con dependencias según la corrida nueva. Fuera: las filas de la matriz y su resumen (no cambian, porque las 9 filas abiertas no dependen de deskops); tocar código o pruebas; cambiar deskops; declarar el retiro.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero el acta completa, en particular la fila de deskops, G4, Lo que falta y el bloque de la corrida de IR13g, y la línea de G4 de la matriz. Para verificar deskops: git -C ../deskops merge-base --is-ancestor 2421ca29 origin/main, y lo mismo con 74ffdb63 y b716bf85, salen con rc 0; grep -n spec2viz ../deskops/.sldb/core/store_index.yaml no muestra ningún enlace de store a spec2viz. Si algo falla, no se marca resuelto: se anota y se reporta. El comprobador es timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb; sus filas no acreditadas deben coincidir con las abiertas de la matriz. Comandos desde la raíz de IR, con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo los dos documentos.
- Los merge-base de 2421ca29, 74ffdb63 y b716bf85 contra origin/main de deskops salen con rc 0, y specir retirement check no lista dependencias de deskops.
- Las filas no acreditadas de specir retirement check coinciden con las filas abiertas de la sección Acreditación (IR13) de la matriz.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

El acta registra a deskops como resuelto con sus commits y trae la corrida nueva; G4 en el acta y en la matriz ya no nombra a graph_ui, deskops ni pron como consumidores pendientes.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir13h-registrar-en-el-acta-que-deskops-ya-no-depende-de-spec2viz-y-actualizar-g4: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

