---
id: task-ir12-renderers-linter-y-recursos-estaticos-de-spec2viz
status: deferred
summary: 'Candidata diferida: cubrir en specIR todos los formatos de salida de spec2viz,
  el linter de Mermaid, el JSON Schema y los recursos empaquetados.'
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ''
history: []
references: []
depends_on:
- task-ir11-compiladores-y-proyecciones-de-spec2viz
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
---

# IR12 Renderers, linter y recursos estáticos de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Candidata diferida. Lo que los usuarios de spec2viz consumen son archivos renderizados. Para retirar spec2viz, specIR tiene que producir cada formato, no solo los que alguien usa hoy.

## Goal

_Describe the concrete result this task must produce._

specIR produce todos los formatos de salida de spec2viz a partir de la representación intermedia, con paridad verificable, y distribuye los recursos que esos formatos necesitan.

## Scope

_State what is in scope and what is out of scope._

Dentro: renderizadores Mermaid, PlantUML, D2, Vega, BPMN y su visor, árbol, HTML de grafo, antonia HTML y salida JSON; linter de Mermaid; export de JSON Schema de specs y de catálogos; recursos empaquetados: plantillas HTML, bpmn-js y los que requiera cada formato; comandos equivalentes a render, lint y schema. Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura.
Fuera: compiladores; sincronización al store, catálogos y consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Tipo sugerido: task.code (el tipo se asigna al autorar la tarea activa con deskops add task --task-type; en una candidata diferida task_type queda vacío). Módulos de renderizado en el paquete specIR que consumen la representación intermedia de la candidata de compiladores; paridad medida con los golden y pruebas de renderizadores de spec2viz ejecutados contra specIR.

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
