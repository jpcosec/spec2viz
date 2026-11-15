---
sldb:
  by: agent
  at: '2026-11-15T22:58:11Z'
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
- src/specir/visual/__init__.py
- src/specir/visual/exceptions.py
- src/specir/visual/ir.py
- src/specir/visual/projections.py
- src/specir/visual/spec_models.py
- src/specir/visual/notation_style.py
- src/specir/visual/renderers/__init__.py
- src/specir/visual/renderers/mermaid.py
- src/specir/visual/renderers/plantuml.py
- src/specir/visual/renderers/d2.py
- src/specir/visual/renderers/vega.py
- src/specir/visual/renderers/bpmn.py
- src/specir/visual/renderers/bpmn_palette.py
- src/specir/visual/renderers/bpmn_viewer.py
- src/specir/visual/renderers/tree.py
- src/specir/visual/renderers/graph_html.py
- src/specir/visual/renderers/antonia_html.py
- src/specir/visual/renderers/json_out.py
- src/specir/visual/renderers/class_diagram.py
- src/specir/visual/renderers/view_mermaid.py
- src/specir/visual/lint_mermaid.py
- src/specir/visual/schema.py
- src/specir/visual/render_file.py
- src/specir/visual/commands.py
- src/specir/visual/templates/default.html
- src/specir/visual/templates/vendor/bpmn-js/LICENSE
- src/specir/visual/templates/vendor/bpmn-js/README.md
- src/specir/visual/templates/vendor/bpmn-js/bpmn-js.css
- src/specir/visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js
- src/specir/visual/templates/vendor/bpmn-js/diagram-js.css
- pyproject.toml
- docs/spec2viz/matriz-de-cobertura.md
- tests/test_imports.py
- tests/visual/render_parity.py
- tests/visual/goldens/spec2viz-2de1056-renders.json
- tests/visual/goldens/spec2viz-2de1056-lint.json
- tests/visual/goldens/spec2viz-2de1056-schema.json
- tests/visual/fixtures/spec2viz/examples/schema/spec2viz.schema.json
- tests/visual/fixtures/spec2viz/examples/schema/sequence.schema.json
- tests/visual/fixtures/spec2viz/examples/schema/class.schema.json
- tests/visual/test_renderers.py
- tests/visual/test_render_parity.py
- tests/visual/test_render_cases.py
- tests/visual/test_render_commands.py
- tests/visual/test_bpmn.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_schema.py
- tests/visual/test_resources.py
- tests/visual/test_visual_names.py
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

Precisiones (preflight): (1) La matriz es docs/spec2viz/matriz-de-cobertura.md (IR07); las filas de esta tarea son SV-A14 (RenderError), SV-A15 y SV-A16 (JSON Schema), SV-C01 a SV-C15 (renderers), SV-D01 (linter), SV-J04 y SV-J05 (bpmn-js y plantilla) y la parte de plantilla de SV-G08; una diferencia se declara en la condición de retiro de su fila, con la prueba que la cubre. La matriz no acredita filas: las cita IR13. (2) La representación intermedia es la de IR11: src/specir/visual/ir.py (dataclasses de spec2viz/ir.py tal cual) y compile_ir de src/specir/visual/compilers; los specs se cargan y validan con sldb.api.notations.load_spec/validate_spec (D3). (3) El corpus de paridad es el de IR11: los specs de spec2viz 2de1056 en tests/visual/fixtures/spec2viz/ con sus rutas; los 36 que validan, dibujados con los nueve renderers, más la página del visor BPMN de cada actividad; los resultados de spec2viz se guardan en tests/visual/goldens/spec2viz-2de1056-renders.json, sus hallazgos de lint en spec2viz-2de1056-lint.json y su JSON Schema en spec2viz-2de1056-schema.json (tests/visual/render_parity.py los regenera y es, junto a parity.py, el único que importa spec2viz). (4) Recursos: los de spec2viz/templates/ copiados byte a byte: default.html y vendor/bpmn-js (bpmn-js 18.31.1, licencia bpmn.io en LICENSE, procedencia en README.md); se declaran como package-data en pyproject.toml. (5) Comandos: src/specir/visual/commands.py migra de spec2viz/cli.py los grupos diagram (render, lint, schema y validate, que es el comando que nombra la cabecera de procedencia) y catalog (schema) con los mismos argumentos y opciones; el script specir apunta a ese grupo hasta que IR13d monte src/specir/cli.py con la taxonomía completa y los alias de primer nivel. render_to_file y la cabecera de procedencia (SV-J03) se migran aquí porque diagram render los necesita; IR13d los expone en la API pública. (6) El selector son los nueve valores de DIAGRAM_RENDERERS de spec2viz/cli.py (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json) con sus extensiones (EXT_MAP) y el renderer por defecto de cada IR (DEFAULT_RENDERER).
Carencia de sldb (pedida a su desk): sldb.api no exporta resolve_style, load_palette ni NotationError (están en sldb.notations), ni AnyDiagram, DiagramType y DiagramStoreEnvelope (en sldb.models.notation.diagram_specs). Hasta que lo haga, src/specir/visual/notation_style.py es el único módulo que importa de sldb.notations y src/specir/visual/spec_models.py, que ya era el de los modelos de D3, añade los tres modelos; tests/test_imports.py acota ambas excepciones.
Transición sin estado de origen (pendiente de IR11): ANY_STATE = "*" pasa a ser parte del contrato de la IR (src/specir/visual/ir.py); mermaid, plantuml y d2 la dibujan saliendo de un único pseudoestado punteado con rótulo «*» (id __any_state), distinto del estado inicial, y un StateIR sin estado inicial no dibuja la flecha inicial. Ningún spec de spec2viz produce esos casos, así que la paridad no cambia.

Precisiones (bundle): (1) La paridad de un par (spec, renderer) que no dibuja es el error: misma clase (RenderError) y mismo mensaje que spec2viz; los goldens guardan {"error": [clase, mensaje]} para esos pares y {"out": salida} para los demás. (2) IR12 edita la matriz solo para declarar sus diferencias en la condición de retiro de la fila (SV-C05: orden del dominio de kindColor en vega) y corregir destinos (SV-C13, SV-C14, SV-D01, SV-J03, pendiente 5); no añade evidencia ni marca filas como cumplidas: eso lo hace IR13 citando las pruebas de tests/visual/. (3) ANY_STATE lo definía projections.py (IR11); IR12 lo mueve a ir.py como parte del contrato de la IR y projections.py lo importa de allí, con el mismo valor. (4) La carencia de sldb no bloquea IR12: queda resuelta con los dos módulos acotados; quitar las excepciones de tests/test_imports.py es trabajo posterior, cuando sldb exporte esos nombres desde sldb.api.notations.

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
