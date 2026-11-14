---
sldb:
  by: agent
  at: '2026-11-12T01:26:15Z'
  authority: generated
  via: save_document_payload
id: task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir11-compiladores-y-proyecciones-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/renderers/__init__.py
- src/specir/visual/renderers/mermaid.py
- src/specir/visual/renderers/plantuml.py
- src/specir/visual/renderers/d2.py
- src/specir/visual/renderers/vega.py
- src/specir/visual/renderers/bpmn.py
- src/specir/visual/renderers/tree.py
- src/specir/visual/renderers/graph_html.py
- src/specir/visual/renderers/antonia_html.py
- src/specir/visual/renderers/json_out.py
- src/specir/visual/lint_mermaid.py
- src/specir/visual/schema.py
- src/specir/visual/templates/default.html
- tests/visual/test_renderers.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_schema.py
- tests/visual/test_resources.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
from_drawer: desk/drawer/tasks/task-ir12-renderers-linter-y-recursos-estaticos-de-spec2viz.md
---

# IR12 Renderers, linter y recursos estáticos de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Lo que los usuarios de spec2viz consumen son archivos renderizados. Para retirar spec2viz, specIR tiene que producir cada formato, no solo los que alguien usa hoy.

## Goal

_Describe the concrete result this task must produce._

specIR produce todos los formatos de salida de spec2viz a partir de la representación intermedia, con paridad verificable, y distribuye los recursos que esos formatos necesitan.

## Scope

_State what is in scope and what is out of scope._

Dentro: renderizadores Mermaid, PlantUML, D2, Vega, BPMN y su visor, árbol, HTML de grafo, antonia HTML y salida JSON; linter de Mermaid; export de JSON Schema de specs y de catálogos; recursos empaquetados: plantillas HTML, bpmn-js y los que requiera cada formato; comandos equivalentes a render, lint y schema. Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura.
Fuera: compiladores; sincronización al store, catálogos y consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulos de renderizado en el paquete specIR que consumen la representación intermedia de la tarea de compiladores; paridad medida con los golden y pruebas de renderizadores de spec2viz ejecutados contra specIR.

## Validation

_List the checks required before this task can close._

- Por cada renderizador, los fixtures de spec2viz producen en specIR una salida idéntica a su golden, o la diferencia está declarada en la matriz de cobertura con su prueba equivalente.
- El linter de Mermaid reporta en specIR los mismos hallazgos que en spec2viz sobre los fixtures de lint.
- El JSON Schema exportado por specIR para specs y catálogos es igual al de spec2viz, o la diferencia está declarada.
- El HTML del visor BPMN y el HTML de grafo generados abren sin recursos externos faltantes (prueba de empaquetado).
- Todos los valores del selector de renderizador de spec2viz existen en specIR.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas de paridad de renderizadores, linter y schema pasan en specIR y sus filas de la matriz de cobertura tienen la condición de retiro cumplida.
