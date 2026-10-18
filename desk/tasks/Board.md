---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-add-d2-renderer-spike-from-existing-ir.md
- desk/tasks/task-sync-golden-plantuml-files.md
- desk/tasks/task-add-render-antonia-html-command.md
- desk/tasks/task-vocabulario-visual-declarativo-notationdoc-glyphdoc-y-linkdoc-sincronizados-al-store.md
- desk/tasks/task-contrato-de-lectura-de-la-notacion-para-graph-ui-y-pilotos-uml-de-clases-y-statechart.md
- desk/tasks/task-auditoria-de-empaquetado-version-rango-de-sldb-metadata-editable-mmdc-import-de-structurednldoc.md
- desk/tasks/task-atributos-de-arista-en-la-vista-multiplicidades-acciones-de-transicion-y-fragmentos-de-secuencia-car.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# spec2viz Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

- Add D2 renderer spike from existing IR [draft] - Prove that spec2viz can target D2 as an additional outward renderer without changing semantic models or compiler behavior.
- Sync golden PlantUML files [draft] - Regenerate each stale golden .puml file by running the current render pipeline against the corresponding YAML fixture.

## Task Details

_Generated from the task references above._

- Add D2 renderer spike from existing IR [draft] - Prove that spec2viz can target D2 as an additional outward renderer without changing semantic models or compiler behavior.
- Sync golden PlantUML files [active] - Regenerate each stale golden .puml file by running the current render pipeline against the corresponding YAML fixture.
- Generate styled HTML diagrams with antonIA aesthetic [active] - Triage and resolve the inbox message: allow spec2viz to generate standalone HTML diagrams that share the premium aesthetic from the reference antonIA HTML file.
- Vocabulario visual declarativo: NotationDoc, GlyphDoc y LinkDoc sincronizados al store [draft] - spec2viz define NotationDoc/GlyphDoc/LinkDoc como modelos sldb, trae notaciones builtin en YAML (uml-class y statechart como pilotos), las valida y las escribe al store; SpecDoc referencia su notacion y SpecNodeDoc lleva el payload del elemento (atributos, metodos, guardas) para que la vista pueda dibujar compartimentos.
- Contrato de lectura de la notacion para graph_ui y pilotos UML de clases y statechart [draft] - Un documento de contrato en spec2viz (docs/notation-contract.md) que fija: como se elige la notacion de un spec, como casa un glifo (model + where, primer match en orden), como casa un link (relation_type del RelationDoc; contains como arista nest), las plantillas de rotulo {campo} sobre el payload de SpecNodeDoc, y la aplicabilidad (modelos y relaciones que nombra la notacion existen en el store). Los dos pilotos sincronizados en el store del repo y visibles en graph_ui /api/graph; la D3 del plan de cierre de graph_ui apuntando a este contrato.
- Auditoria de empaquetado: version, rango de sldb, metadata editable, mmdc, import de StructuredNLDoc [draft] - pyproject y CHANGELOG alineados (version 0.2.0, structuredLanguageDB>=0.1.10), instalacion editable refrescada, mmdc documentado en el README como dependencia externa opcional, y el import de StructuredNLDoc via sldb.api en cuanto sldb lo exponga (pedido a sldb-04).
- Atributos de arista en la vista: multiplicidades, acciones de transicion y fragmentos de secuencia; carriles y grilla con graph_ui [draft] - Cada arista del spec conserva sus atributos en el store (campo libre de RelationDoc pedido a sldb-04, o alternativa acordada), resolve_view los expone (link.data, source_label/target_label en LinkDoc, fragments de secuencia por group) y el contrato fija como se ordenan carriles (participantes) y grilla (etapas por data.order, filas por nest). graph_ui los consume.
