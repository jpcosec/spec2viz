---
sldb:
  by: agent
  at: '2026-11-21T09:27:07Z'
  authority: generated
  via: save_document_payload
id: task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- tests/test_matriz_cobertura_spec2viz.py
- tests/visual/goldens/spec2viz-2de1056-oracle.json
- tests/visual/oracle.py
- tests/visual/parity.py
- tests/visual/render_parity.py
- tests/visual/test_catalog_parity.py
- tests/visual/test_cli.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_render_cases.py
- tests/visual/test_render_commands.py
- tests/visual/test_render_parity.py
- tests/visual/test_resources.py
- tests/visual/test_schema.py
- tests/visual/test_sync_generation_parity.py
- tests/visual/test_visual_names.py
- tests/visual/test_visual_parity.py
- c47111de57c53e75a15a565ec945b73695de96c8
depends_on: []
pills: []
files:
- tests/test_matriz_cobertura_spec2viz.py
- tests/visual/goldens/spec2viz-2de1056-oracle.json
- tests/visual/oracle.py
- tests/visual/parity.py
- tests/visual/render_parity.py
- tests/visual/test_catalog_parity.py
- tests/visual/test_cli.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_render_cases.py
- tests/visual/test_render_commands.py
- tests/visual/test_render_parity.py
- tests/visual/test_resources.py
- tests/visual/test_schema.py
- tests/visual/test_sync_generation_parity.py
- tests/visual/test_visual_names.py
- tests/visual/test_visual_parity.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz
---

# Las pruebas de paridad de IR comparan contra goldens congelados de spec2viz y dejan de importarlo (acta, punto 6)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: specir retirement check cuenta 43 dependencias de IR sobre spec2viz, todas en pruebas: los oráculos de paridad de tests/visual (render_parity.py 13, test_sync_generation_parity.py 9, test_catalog_parity.py 7, test_render_parity.py 3, parity.py 3, test_visual_parity.py 2, y una en test_schema.py, test_resources.py, test_render_commands.py, test_render_cases.py, test_lint_mermaid.py y tests/test_matriz_cobertura_spec2viz.py). El acta de retiro (docs/spec2viz/acta-de-retiro.md, 'Lo que falta', punto 6) pide quitarlos o congelarlos. Ya hay goldens grabados de spec2viz 2de1056 en tests/visual/goldens/ (spec2viz-2de1056*.json).

## Goal

_Describe the concrete result this task must produce._

Ningún archivo de IR importa ni invoca spec2viz: specir retirement check no lista dependencias de IR. Cada comparación con spec2viz en vivo pasa a comparar contra un golden versionado en tests/visual/goldens/, grabado desde spec2viz (el checkout /mnt/ssd/proyectos/SLDB_1/spec2viz, con su commit en el nombre del archivo, como los spec2viz-2de1056*.json) con un script de grabación que vive fuera de tests/ (en runs/<run>/, que el comprobador no audita), y la prueba carga el golden sin importar spec2viz. Si un caso ya está cubierto por un golden existente, la prueba en vivo se borra. La cobertura de la paridad no baja: los casos que hoy pasan con spec2viz instalado siguen comprobados. tests/test_matriz_cobertura_spec2viz.py deja de importar spec2viz.cli (usa el golden o una lista congelada de comandos).

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/visual/*parity*.py, tests/visual/parity.py, tests/visual/render_parity.py, las líneas que importan spec2viz en test_schema.py, test_resources.py, test_render_commands.py, test_render_cases.py, test_lint_mermaid.py, tests/test_matriz_cobertura_spec2viz.py, tests/visual/goldens/ y el script de grabación en el run dir. Fuera: src/, la matriz, el acta, el store de spec2viz y el repo spec2viz (solo se lee).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: inventario: correr la suite de paridad con spec2viz instalado (pytest -m parity) y anotar qué casos pasan hoy. p2: por módulo, grabar los goldens que falten con el script de grabación (en el run dir) y cambiar la prueba a leer el golden. p3: borrar imports y pytest.importorskip('spec2viz'). p4: correr de nuevo: los mismos casos pasan sin spec2viz instalado. p5: specir retirement check con las rutas (deskops=/mnt/ssd/proyectos/SLDB_1/deskops graph_ui=/mnt/ssd/proyectos/SLDB_1/UIs/graph_ui pron=/mnt/ssd/proyectos/SLDB_1/pron sldb=/mnt/ssd/proyectos/SLDB_1/sldb spec2viz/.sldb=/mnt/ssd/proyectos/SLDB_1/spec2viz/.sldb) sin dependencias de IR, salida en el run dir. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual tests/test_matriz_cobertura_spec2viz.py

## Done When

_Name the observable condition that makes the task complete._

tests/visual pasa sin spec2viz importable con el mismo número de casos de paridad que antes pasaban con él, y specir retirement check no lista ninguna dependencia de IR.
