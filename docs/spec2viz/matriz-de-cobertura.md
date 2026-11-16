# Matriz de cobertura de spec2viz

Plan de cobertura para retirar spec2viz (tarea IR07). Cada capacidad de spec2viz tiene una fila con su
**modo** y su **condición de retiro**. Esta matriz **no acredita nada**: no hay columna de evidencia y
ninguna fila se da por cumplida. La tarea final IR13 añade por fila la prueba que acredita la cobertura
(después de IR13a, IR13b, IR13c e IR13d) y es la única que puede marcar una fila como cumplida.
IR13 lo hace en la sección «Acreditación (IR13)», al final: estado de cada fila (cumplida o abierta), la
prueba que la acredita y lo que falta. Los modos y las condiciones de retiro de IR07 no cambian.

- Revisión inventariada de spec2viz: commit `2de1056` del repo `spec2viz` (versión 0.2.0 en su
  `pyproject.toml`). La ayuda del CLI instalado (`spec2viz --help` y la de cada subgrupo) coincide con
  `spec2viz/spec2viz/cli.py` de esa revisión.
- Revisión de sldb consultada: rama main de `sldb` en `641ecdfa`. Plan de sldb que absorbe lo genérico:
  `sldb/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/` (`alcance.md`, `brief.md`, `decisiones.md`).
- Decisión vigente (JP, 2026-11-15): lo genérico va a sldb; specIR es adaptador y mapeo de dominio y
  conserva la capa visual (compiladores en IR11, renderers en IR12).
- La decisión sobre el papel del YAML de spec frente al grafo está en
  `docs/decisiones/fuente-de-verdad-del-diagrama.md` y en el atom
  `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`.
  **Aceptada por JP el 2026-11-15** (vía supervisor): el YAML del spec queda como formato de autoría e
  intercambio subordinado al grafo. La propuesta de IR07 (`atom-propuesta-pendiente-de-jp-…`) se fusionó en
  ese atom y queda como redirección. Solo las filas marcadas con † dependían de ella.
- El procedimiento del gate está en `docs/spec2viz/gate-de-retiro.md`; la lista comprobable está al final
  de este documento.

## Modos

| Modo | Qué significa | Qué debe citar la fila |
|---|---|---|
| migrar tal cual | El código pasa a specIR (capa visual) con sus pruebas de spec2viz portadas. | Tarea de specIR que lo migra y pruebas de spec2viz que se portan. |
| reemplazar | Otra arquitectura o experiencia con resultado equivalente. | Sustituto y prueba que demostrará la equivalencia. |
| usar sldb directamente | Ya vive en SLDB; se consume por su API, su CLI o `sldb serve`, sin envoltorio ni reexportación en specIR. | Operación pública de SLDB que la respalda. |
| migrado a sldb | Pieza no visual ni de dominio; su código pasa a sldb con sus pruebas portadas y specIR la consume desde allí. | Tarea de sldb que la migra y pruebas de spec2viz que se portan a sldb. |

Tareas citadas (ids completos):

| Abreviatura | Tarea | Desk |
|---|---|---|
| D1 | `task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo` (espejo en IR: `task-espejo-sldb-specsync-en-sldb-api-notations-d1`) | sldb |
| D2 | `task-migrar-a-sldb-el-generador-de-spec-de-componentes-desde-un-grafo-y-desde-el-ast-de-python-d2-b4` (espejo: `task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2`) | sldb |
| D3 | `task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp` (espejo: `task-espejo-sldb-modelos-de-spec-por-tipo-de-diagrama-d3`) | sldb |
| D4 | `task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4` (espejo: `task-espejo-sldb-emparejamiento-de-átomos-en-sldb-api-matching-d4`) | sldb |
| IR11 | `task-ir11-compiladores-y-proyecciones-de-spec2viz` | IR |
| IR12 | `task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz` | IR |
| IR13a | `task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs` | IR |
| IR13b | `task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos` | IR |
| IR13d | `task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual` | IR |
| IR13 | `task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz` | IR |

IR13c (notaciones y paletas) se retiró porque era un envoltorio de `sldb notations`: sus filas están en
modo «usar sldb directamente» y la prueba de paridad de esas filas la aporta IR13 (ver «Pendientes de
derivación»).

Rutas: las de spec2viz son relativas a la raíz del repo `spec2viz` (`spec2viz/<módulo>.py` es el paquete;
`tests/` sus pruebas). Las pruebas citadas son las de `spec2viz/tests/` en la revisión inventariada.

## Matriz

### A. Modelos de spec, carga, validación y JSON Schema

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-A01 | Modelo de spec de diagrama de clases (paquetes, herencia, sobrecargas) | `spec2viz/models/class_diagram.py` | migrado a sldb | D3: subpaquete de modelos de diagrama junto a SpecDoc en sldb | Pasan en sldb, portadas por D3: de `tests/test_class_diagram.py` test_semantic_errors_are_rejected, test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed, test_overloads_with_distinct_parameter_types_are_allowed y test_invalid_schema_fails_at_load; de `tests/test_class_packages.py` test_typed_validation y test_package_id_cannot_be_a_class_id. specIR no define el modelo (prueba de imports y nombres de IR11). |
| SV-A02 | Modelo de spec de secuencia | `spec2viz/models/sequence.py` | migrado a sldb | D3 | `tests/test_models_sequence.py` (3) portado a sldb y en verde; specIR importa el modelo de sldb (IR11). |
| SV-A03 | Modelo de spec de estado | `spec2viz/models/state.py` | migrado a sldb | D3 | `tests/test_models_state.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A04 | Modelo de spec de componentes | `spec2viz/models/component.py` | migrado a sldb | D3 | `tests/test_models_component.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A05 | Modelo de spec de actividad (particiones, merge, notas) | `spec2viz/models/activity.py` | migrado a sldb | D3 | `tests/test_models_activity.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A06 | Modelo de spec de despliegue (nodos anidados, communication paths) | `spec2viz/models/deployment.py` | migrado a sldb | D3 | `tests/test_models_deployment.py` (4) portado a sldb y en verde; ídem IR11. |
| SV-A07 | Modelo de spec de matriz (component_view_matrix) | `spec2viz/models/matrix.py` | migrado a sldb | D3 | `tests/test_models_matrix.py` (4) portado a sldb y en verde; ídem IR11. |
| SV-A08 | Modelo de spec de reflexión (enforcement) | `spec2viz/models/reflection.py` | migrado a sldb | D3 | spec2viz no tiene prueba de modelo propia de reflexión: la condición es la comparación de errores de D3 (misma clase y mismo texto de error) sobre todos los ejemplos y fixtures de spec2viz, que incluye `examples/reflection/`; specIR importa el modelo de sldb (IR11). |
| SV-A09 | Modelo base común (`BaseDiagram`, metadata, `DiagramType`) | `spec2viz/models/base.py` | migrado a sldb | D3 (DiagramType se reutiliza de `sldb.notations.diagram_type`, no se migra) | `tests/test_base_model.py` (3) portado a sldb y en verde. |
| SV-A10 | Modelo de catálogo (`vistas.yml` y stores jerárquicos de diagramas) | `spec2viz/models/catalog.py` | migrado a sldb | D3 | El modelo valida en sldb los fixtures de catálogo de spec2viz (`examples/catalog/`, `docs/architecture/spec2viz/vistas.yml`) con los mismos errores (comparación de errores de D3). |
| SV-A11 | Carga de un spec desde YAML (`load`) | `spec2viz/loader.py` | migrado a sldb | D3: `sldb.api.notations.load_spec` | `tests/test_loader.py` (16) portado a sldb y en verde. |
| SV-A12 | Validación semántica de un spec (`validate`) | `spec2viz/validator.py` | migrado a sldb | D3: `sldb.api.notations.validate_spec` | `tests/test_validator.py` (19) portado a sldb y en verde. |
| SV-A13 | Errores de carga y validación (`ParseError`, `ValidationError` y su jerarquía) | `spec2viz/exceptions.py` | migrado a sldb | D3: `ParseError` nueva bajo `NotationError`; el resto se reutiliza de `sldb.notations.exceptions` | `tests/test_exceptions.py` (2), solo los asertos de ParseError y ValidationError, portado a sldb y en verde. |
| SV-A14 | Errores de la capa visual (`Spec2VizError`, `CompileError`, `RenderError`) | `spec2viz/exceptions.py` | migrar tal cual | IR11 (CompileError) e IR12 (RenderError, raíz visual) | Los asertos de `tests/test_exceptions.py` sobre esas tres clases pasan en specIR con sus nombres; las pruebas de compiladores y renderers portadas levantan las mismas clases. |
| SV-A15 | Export de JSON Schema de specs (por tipo o todos) | `spec2viz/schema.py` | migrar tal cual | IR12 (`src/specir/visual/schema.py`) | El schema que exporta specIR es igual al de spec2viz para cada tipo (prueba de schema de IR12); pasan portadas test_json_schema_for_all_types, test_json_schema_for_specific_type y test_write_json_schema de `tests/test_api.py`, test_schema_stdout, test_schema_outfile y test_schema_invalid_type_fails de `tests/test_cli.py`, y test_schema_examples_match_generated_output y test_every_model_field_has_a_description de `tests/test_packaging.py`. |
| SV-A16 | Export de JSON Schema de catálogos y stores jerárquicos | `spec2viz/schema.py`, `spec2viz/cli.py` (`catalog schema`) | migrar tal cual | IR12 | Igual a spec2viz; pasan portadas test_schema_diagram_store_stdout y test_catalog_schema_stdout de `tests/test_cli.py`. |
| SV-A17 | Modelos de store de spec2viz (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) | `spec2viz/sldb_models.py` | usar sldb directamente | Modelos públicos de sldb: `sldb.models.notation.spec_doc.SpecDoc`, `spec_node_doc.SpecNodeDoc`, `notation_doc.NotationDoc`, `glyph_doc.GlyphDoc`, `link_doc.LinkDoc`, `palette_doc.PaletteDoc`, `view_doc.ViewDoc` | Los casos de `tests/test_view_doc.py` (3) pasan importando `ViewDoc` de sldb; specIR no define ninguna clase con esos nombres (IR11); ningún store registra `spec2viz.sldb_models` (gate G5). |

### B. Representación intermedia y compiladores (IR11)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-B01 | Representación intermedia visual (una dataclass por tipo de diagrama, `EnforcementArtifact`) | `spec2viz/ir.py` | migrar tal cual | IR11 | `tests/test_ir.py` (3) portado a specIR y en verde. |
| SV-B02 | Despacho de compilación por tipo (`compile_ir`) | `spec2viz/compilers/__init__.py` | migrar tal cual | IR11 | test_compile_* de `tests/test_api.py` (6) y `tests/test_compilers.py` (17) portados y en verde con la normalización de IR11. |
| SV-B03 | Compilador de clases | `spec2viz/compilers/class_diagram.py` | migrar tal cual | IR11 | Pasan en specIR las pruebas de compilación y render de `tests/test_class_diagram.py` y `tests/test_class_packages.py` que no porta D3 (las que invocan compile_ir o render). |
| SV-B04 | Compilador de secuencia | `spec2viz/compilers/sequence.py` | migrar tal cual | IR11 | Casos de secuencia de `tests/test_compilers.py` portados; IR equivalente según la normalización de IR11. |
| SV-B05 | Compilador de estado | `spec2viz/compilers/state.py` | migrar tal cual | IR11 | Casos de estado de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B06 | Compilador de componentes | `spec2viz/compilers/component.py` | migrar tal cual | IR11 | Casos de componentes de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B07 | Compilador de actividad (particiones, merge, notas) | `spec2viz/compilers/activity.py` | migrar tal cual | IR11 | Casos de actividad de `tests/test_compilers.py` y `tests/test_activity_lanes.py` (10) portados; IR equivalente. |
| SV-B08 | Compilador de despliegue (anidado, communication paths, deploy/manifest) | `spec2viz/compilers/deployment.py` | migrar tal cual | IR11 | Casos de despliegue de `tests/test_compilers.py` y `tests/test_deployment_nested.py` (6) portados; IR equivalente. |
| SV-B09 | Compilador de matriz | `spec2viz/compilers/matrix.py` | migrar tal cual | IR11 | Casos de matriz de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B10 | Compilador de reflexión (artefacto de enforcement) | `spec2viz/compilers/reflection.py` | migrar tal cual | IR11 | `tests/test_reflection_compiler.py` (1) portado y en verde. |

### C. Renderizadores (IR12)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-C01 | Despacho de render, selector `--renderer`/`--backend` (9 valores), extensiones y renderer por defecto por tipo | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/__init__.py`) | Los 9 valores (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json) existen en specIR; test_render_str, test_render_dict y test_render_mermaid_override de `tests/test_api.py` y test_render_override y test_render_backend_alias de `tests/test_cli.py` portados y en verde. |
| SV-C02 | Mermaid | `spec2viz/renderers/mermaid.py` | migrar tal cual | IR12 | Casos mermaid de `tests/test_renderers.py` (golden idéntico o diferencia declarada aquí con su prueba), más los de `tests/test_activity_lanes.py` y `tests/test_deployment_nested.py`. |
| SV-C03 | PlantUML | `spec2viz/renderers/plantuml.py` | migrar tal cual | IR12 | Casos plantuml de `tests/test_renderers.py`, `tests/test_activity_lanes.py` y `tests/test_deployment_nested.py`. |
| SV-C04 | D2 | `spec2viz/renderers/d2.py` | migrar tal cual | IR12 | Casos d2 de `tests/test_renderers.py`, `tests/test_activity_lanes.py`, `tests/test_deployment_nested.py` y test_render_d2 de `tests/test_cli.py`. |
| SV-C05 | Vega (matriz) | `spec2viz/renderers/vega.py` | migrar tal cual | IR12 | Casos vega de `tests/test_renderers.py` y test_render_to_file_vega de `tests/test_api.py`. Diferencia declarada (IR12): spec2viz listaba el dominio de la escala `kindColor` en el orden de un set, que cambia con `PYTHONHASHSEED`; specIR lo lista en orden de primera aparición y el color de cada kind es el mismo. Prueba: test_vega_lists_the_kinds_in_order_of_first_appearance y la paridad de `tests/visual/test_render_parity.py`, que compara esa escala como correspondencia kind → color. |
| SV-C06 | BPMN (XML con DI) | `spec2viz/renderers/bpmn.py` | migrar tal cual | IR12 | `tests/test_bpmn.py` (26), parte XML y DI, portado y en verde. |
| SV-C07 | Visor BPMN offline (bpmn-js embebido, leyenda, metadata, panel) | `spec2viz/renderers/bpmn_viewer.py` | migrar tal cual | IR12 | Casos del visor de `tests/test_bpmn.py`; la prueba de recursos de IR12 abre el HTML sin recursos externos faltantes. |
| SV-C08 | Paleta BPMN in Color compartida por renderer y visor | `spec2viz/renderers/bpmn_palette.py` | migrar tal cual | IR12 | Mismos colores en XML y visor sobre los fixtures de `tests/test_bpmn.py`. |
| SV-C09 | Árbol (HTML colapsable) | `spec2viz/renderers/tree.py` | migrar tal cual | IR12 | Casos tree de `tests/test_renderers.py` portados. |
| SV-C10 | HTML de grafo (DOM puro, sin CDN) | `spec2viz/renderers/graph_html.py` | migrar tal cual | IR12 | Casos graph de `tests/test_renderers.py` y test_render_to_file_component de `tests/test_api.py`; abre desde file:// sin recursos externos (prueba de recursos de IR12). |
| SV-C11 | antonia-html | `spec2viz/renderers/antonia.py` | migrar tal cual | IR12 | Casos antonia de `tests/test_renderers.py` y test_render_antonia_html de `tests/test_cli.py`. |
| SV-C12 | Salida JSON (`JsonRenderer`, artefacto `.artifact.json`) | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`json_out`) | test_render_json_reflection_artifact de `tests/test_cli.py` portado y en verde. |
| SV-C13 | Backends UML de sintaxis para el ClassIR (mermaid y plantuml de clases) | `spec2viz/renderers/class_diagram.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/class_diagram.py`) | Casos de clases de `tests/test_renderers.py`, `tests/test_class_diagram.py` y `tests/test_class_packages.py` con render. |
| SV-C14 | Mermaid desde una vista resuelta (glifo, forma, keyword, compartimentos, estilo) | `spec2viz/renderers/view_mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/view_mermaid.py`), consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde contra la vista resuelta de sldb. |
| SV-C15 | Prueba de regresión de render a archivo | `spec2viz/__init__.py` (`render_to_file`) | migrar tal cual | IR12 e IR13d | `tests/test_rendering_bug.py` (1) portado y en verde. |

### D. Linter

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-D01 | Linter de Mermaid (heurísticas y pasada real con mmdc si está) | `spec2viz/linters/mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/lint_mermaid.py`; la variable `SPECIR_MMDC` sustituye a `SPEC2VIZ_MMDC`, que sigue valiendo) | `tests/test_mermaid_mmdc.py` (4) portado y en verde; los mismos hallazgos que spec2viz sobre los fixtures de lint (prueba de lint de IR12). |

### E. Sincronización al store (SpecSync)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-E01 | SpecSync: materializar un spec como SpecDoc, SpecNodeDoc y RelationDoc, crear el RelationTypeDoc que falte y borrar lo que salió del spec; informe (`format_report`) | `spec2viz/sldb_sync.py` | migrado a sldb | D1: `SpecSync`, `sync_spec` en `sldb.api.notations`; `sldb notations sync --spec`. Reutiliza `StoreWriter` y `SyncReport` de sldb | `tests/test_sldb_sync.py` (16) portado a sldb, contra store real y sin mocks, en verde; informe igual campo a campo al de spec2viz sobre los mismos specs (D1); specIR llama a la API de sldb sin envoltorio (IR13a): `tests/visual/test_sync_generation_parity.py` sincroniza con sldb y con spec2viz los 14 specs válidos de `tests/fixtures/` y los ARQ/FLOW de `tests/test_sldb_sync.py` (con un resync que quita un nodo) y compara informes y SpecDoc, SpecNodeDoc, RelationDoc, RelationTypeDoc y documentos de notación; borrado al resincronizar y RelationTypeDoc de relación no builtin con `check_edges` limpio, contra store real. Diferencia declarada: la descripción del RelationTypeDoc que crea la sincronización ya no termina en «de spec2viz». |
| SV-E02 | Sincronización de notaciones y paletas al store (`NotationSync`, `PaletteSync`, `format_notation_report`) | `spec2viz/sldb_sync.py` | usar sldb directamente | `sldb.api.notations.NotationSync`, `PaletteSync`, `sync_notation`, `sync_palette`; CLI `sldb notations sync --notation/--palette` | Los casos de notación y paleta de `tests/test_sldb_sync.py` y `tests/test_style_palette.py` que sincronizan pasan llamando a la API de sldb, sin envoltorio en specIR. |

### F. Generación de specs

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-F01 | from-graph: compilar el grafo de un store (edge index) o un snapshot node-link en un spec de componentes | `spec2viz/graph_import.py` | migrado a sldb | D2: `component_spec_from_graph` en `sldb.api.notations`; `sldb notations from-graph --snapshot/--store` | `tests/test_graph_import.py` (21) portado a sldb y en verde; todo spec generado valida con el modelo de componentes de D3. IR13a (`tests/visual/test_sync_generation_parity.py`): sobre los snapshots node-link de `tests/test_graph_import.py` (el de documentos y `PY_GRAPH`) y sobre el edge index de un store sincronizado, `load_node_link`, `load_node_link_graph`, `index_graph` y `component_spec_from_graph` dan lo mismo que spec2viz, y cada spec valida con `load_spec`/`validate_spec`; sin diferencias. |
| SV-F02 | Generar un spec de componentes desde el AST de Python | `spec2viz/generators/python_ast.py` | migrado a sldb | D2: `component_spec_from_python` sobre `sldb.code.scan_tree`, `write_component_spec`; `sldb notations from-graph --python` | spec2viz no tiene pruebas de este generador: la condición es la prueba nueva de D2 que compara con `generate_python_ast_spec` de spec2viz sobre un árbol pequeño (mismos módulos, clases y relaciones defines) y valida con el modelo de D3. IR13a (`tests/visual/test_sync_generation_parity.py`) compara sobre un paquete real (`src/specir`): módulos, clases y aristas defines idénticos y en el mismo orden; el spec valida. Diferencias declaradas en las aristas imports, porque sldb las lee de `sldb.code.scan_tree`: cuenta los `import x` (spec2viz solo los `from x import y`), resuelve los imports relativos contra el paquete del módulo (spec2viz emite el nombre sin resolver), no repite una arista por sentencia y no lee los `from x import y` anidados bajo el nivel superior del módulo (en funciones, `if` o `try`; spec2viz recorre todo el árbol). Lo último es una pérdida pedida al desk de sldb (`code/scan-tree-nested-imports`); los nodos external siguen a las aristas. |

### G. Catálogos

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-G01 | Construcción del catálogo HTML autocontenido desde un `vistas.yml` o un store de stores (marca, subtítulo, plantilla local, `project.yml`, secciones HTML, anchors únicos) | `spec2viz/orchestrator.py` | migrar tal cual | IR13b con los renderers de IR12 | test_build_command* (7), test_catalog_build_alias_matches_legacy_build y test_build_command_reports_errors de `tests/test_cli.py` portados y en verde; mismas vistas, categorías y navegación que spec2viz sobre el fixture (IR13b). IR13b (`tests/visual/test_catalog.py`, sección de `tests/test_cli.py`): los 9 casos de build portados sobre la API (`specir.visual.catalog.build_catalog`/`render_catalog`; el comando, el alias `build` y sus mensajes «Rendered catalog» y «Error building catalog» son de IR13d; el error de construcción es la excepción). `tests/visual/test_catalog_parity.py`: la página es la de spec2viz byte a byte sobre `docs/architecture/vistas.yml` y `examples/catalog/` de spec2viz, sobre un proyecto sincronizado, stores de stores con overrides, `project.yml`, fragmentos y fuentes de todo tipo; diferencia declarada: los avisos de átomos y cobertura son findings de sldb (`level`, `code`, `subject`, `what`, `fix`) donde spec2viz escribía `{scope, message}`, y se comparan por su texto. `test_the_built_catalog_opens_without_missing_resources`: ninguna referencia local ni anchor roto (mermaid, vega y fuentes por CDN, igual que spec2viz). IR13d: `specir catalog build` y el alias `specir build` con sus mensajes; test_catalog_build_alias_matches_legacy_build, los test_build_command* (7) y test_build_command_reports_errors de `tests/test_cli.py` portados sobre el comando en `tests/visual/test_cli.py`. |
| SV-G02 | Registro `vistas.yml` y stores jerárquicos de diagramas: regla de rutas de `src`, `mmd`, `specs` y `notation` | `spec2viz/catalog_paths.py` | migrar tal cual | IR13b | `tests/test_catalog_paths.py` (9) portado y en verde. IR13b: la regla de rutas ya vive en sldb (`sldb.api.notations.catalog_paths`, D1) y specIR la usa sin copiarla; el cargador del registro y de los stores jerárquicos es `specir.visual.catalog.loader`. `tests/test_catalog_paths.py` (9) portado en `tests/visual/test_catalog.py` contra `catalog_paths` de sldb y `sldb notations sync --catalog [--check]`. |
| SV-G03 | Vistas del catálogo desde la vista resuelta (misma fuente que graph_ui) | `spec2viz/catalog_views.py` | migrar tal cual | IR13b, consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde (compartido con SV-C14). IR13b: `specir.visual.catalog.views` sobre `resolve_view` y `SpecSync` de sldb y `view_to_mermaid` de IR12; los 4 casos de `catalog build` portados en `tests/visual/test_catalog.py` (los dos que usaban monkeypatch se rehacen con una notación que solo vive en el store y con un spec que no es grafo) y los mismos tableros que spec2viz en `tests/visual/test_catalog_parity.py` (`test_resolved_views_are_spec2viz_s`, `test_the_catalog_of_a_synced_project_is_spec2viz_s`). |
| SV-G04 | Sincronización del catálogo al store (`catalog sync`: cada spec del `vistas.yml` con su notación y metadata) | `spec2viz/sldb_sync.py` (`sync_catalog`) | migrado a sldb | D1: `sync_catalog`; `sldb notations sync --catalog` (con `--prune` para borrar los SpecDoc que salieron) | `tests/test_catalog_notation.py` (6) portado a sldb y en verde; no escribe nada si una vista falla (IR13b). IR13b: `tests/test_catalog_notation.py` (6) portado en `tests/visual/test_catalog.py` sobre `sldb notations sync --catalog`; `tests/visual/test_catalog_parity.py` `test_catalog_sync_leaves_what_spec2viz_leaves` (mismos documentos que spec2viz sobre su `docs/architecture/vistas.yml`, comparación de IR13a) y `test_a_failing_view_makes_both_write_nothing`; `tests/visual/test_catalog.py` `test_a_failing_view_writes_nothing_even_after_valid_ones`. |
| SV-G05 | Validación del catálogo (`catalog validate`: specs existen y validan, notaciones del tipo correcto) | `spec2viz/sldb_sync.py` (`check_catalog`) | migrado a sldb | D1: `check_catalog`; `sldb notations sync --catalog --check` | Casos de validación de `tests/test_catalog_notation.py` portados a sldb; mismos errores tipados que spec2viz (IR13b). IR13b: `tests/visual/test_catalog_parity.py` compara `check_catalog` de sldb con el de spec2viz entrada por entrada (vista, spec, clase y mensaje del error) sobre los registros de `test_catalog_paths` y `test_catalog_notation` (rutas faltantes y ambiguas, notación inexistente, de otro tipo o solo del store) y sobre `docs/architecture/vistas.yml` de spec2viz; sin diferencias. |
| SV-G06 | Servir el catálogo en local con autoguardado de anotaciones (`catalog serve`) | `spec2viz/cli.py` (`catalog_serve`) | reemplazar | Sustituto: `sldb serve` (lectura de documento por id y escritura con guarda de hash, comprobado por D4 paso 7) más el JS del catálogo de specIR (IR13b) | Prueba de equivalencia: IR13b demuestra que una anotación hecha con el catálogo servido por `sldb serve` queda guardada y reaparece al recargar. Si D4 concluye que `sldb serve` no alcanza, la fila no se cumple hasta que sldb resuelva la nota `serve/annotation-autosave-gap`. IR13b: `sldb serve` alcanza, sin nota. specIR guarda las anotaciones de un catálogo en un documento `CatalogAnnotationsDoc` (modelo de specIR registrado con `add_model`) y la página las lee con `GET /document?id=` y las guarda con `POST /save` y `expected` (script `templates/annotations-sldb.js`, embebido con `render_catalog(..., annotations=AnnotationsTarget(...))` o por la URL `?sldb=&annotations=`). `tests/visual/test_catalog_annotations.py`: con un `sldb serve --cors` real, el código de la página corrido en node guarda una anotación, que reaparece al recargar (proceso nuevo, `localStorage` vacío) y queda en el store; una página con la guarda vieja (409) mezcla y reintenta. Diferencia declarada: spec2viz escribía `comentarios-arquitectura.json` junto al HTML. |
| SV-G07 | Inyección de átomos en el HTML del catálogo (`render_deskops`, `build_deskops`, `split_shared_atoms`, adaptador `CatalogItem`) | `spec2viz/deskops.py` | migrar tal cual | IR13b (capa visual; D4 lo deja fuera de sldb) | `tests/test_deskops.py` (7) y, de `tests/test_atoms_matching.py`, test_split_shared_atoms_emits_repeated_payload_once y test_catalog_build_embeds_atoms_once_and_honors_atoms_tag, portados y en verde. IR13b: `specir.visual.catalog.atoms` (adaptador de la vista del catálogo a `SpecView`, descubrimiento del store de la vista, `split_shared_atoms`, inyección) sobre `sldb.api.matching`. Portados en `tests/visual/test_catalog.py`: `tests/test_deskops.py` (7; los dos de `parse_atoms` contra sldb, el de cobertura a través del catálogo, el del store con un store real en `tests/visual/test_catalog_parity.py`) y los dos casos de `tests/test_atoms_matching.py`. `tests/visual/test_catalog_parity.py`: los mismos `ATOMS_DB`, `ATOMS_BY_VIEW`, `ATOMS_EXPLICIT`, `ATOMS_LINKED`, `REFS_EXPLICIT` y `COVERAGE_BY_VIEW` que spec2viz (carpeta de átomos, filtro por tags, explícitos, desconocidos, átomos y refs del store de la vista). |
| SV-G08 | Plantilla HTML del catálogo, incluido el emparejamiento difuso en el navegador (`findAtomData`, `normKey`) y las pestañas por átomo | `spec2viz/templates/default.html` | migrar tal cual | IR12 (`src/specir/visual/templates/default.html`) e IR13b | Los casos de `tests/test_atoms_matching.py` que ejecutan la plantilla con node y test_tabs_follow_the_target_atom portados y en verde; `label_key` de D4 sigue coincidiendo con `normKey`. IR13b (`tests/visual/test_catalog.py`): los 7 casos de emparejamiento en el navegador, los 6 de markdown de átomos y `test_tabs_follow_the_target_atom` portados sobre la plantilla de specIR. `label_key` de D4 coincide con `normKey` salvo en `_`: `label_key` lo conserva y `normKey` lo separa (un elemento sin label con `_` en su id no encuentra su átomo explícito; spec2viz tenía el mismo defecto). Lo arregló sldb en `06dbcf02` (pedido `matching/label-key-underscore`, nota 20261115-214942) y el xfail estricto de `test_label_key_of_sldb_splits_underscores_like_norm_key` se quitó en `4dc8946`. |

### H. Notaciones, paletas y estilo (usar sldb directamente)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-H01 | Modelo, carga y validación de notaciones (NotationDoc, GlyphDoc, LinkDoc en YAML; `where` en la gramática de `sldb find --where`) | `spec2viz/notation.py` | usar sldb directamente | `sldb.notations.load_notation`, `sldb.notations.NotationSpec` | Los casos de `tests/test_notation.py` (14) pasan contra `sldb.notations` sin envoltorio en specIR. |
| SV-H02 | Notaciones builtin (8) y notación por defecto por tipo | `spec2viz/notations/*.yml`, `DEFAULT_NOTATIONS` | usar sldb directamente | `sldb.notations.builtin_notations`, `sldb.notations.DEFAULT_NOTATIONS` | Las 8 notaciones de spec2viz (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence) aparecen en `sldb notations list` y su contenido valida igual. |
| SV-H03 | Vista resuelta de un spec (glifo por nodo, link por relación, leyenda) y de documentos sin SpecDoc | `spec2viz/notation_view.py` (`resolve_view`, `resolve_documents`) | usar sldb directamente | `sldb.api.notations.resolve_view`, `sldb.api.notations.resolve_documents`; CLI `sldb notations view` y `sldb notations resolve` | `tests/test_notation_view.py` (11) y `tests/test_view_contract_resolved.py` (2) pasan contra la API de sldb; graph_ui ya no importa `spec2viz.notation_view` (gate G4). IR13g: se cumple; graph_ui master `79d63ee` (closeout `c9b09f7`) usa `sldb.api.notations` y ya no importa ni declara spec2viz (ver «Acreditación (IR13)»). |
| SV-H04 | Modelo, carga y validación de paletas, con contraste WCAG (trazo ≥ 3:1, texto ≥ 4.5:1, forma+icono distintos por kind) | `spec2viz/palette.py` | usar sldb directamente | `sldb.notations.load_palette`, `sldb.notations.PaletteSpec`, `sldb.notations.contrast` | Los casos de paleta y contraste de `tests/test_style_palette.py` pasan contra `sldb.notations`. |
| SV-H05 | Paleta builtin `default` | `spec2viz/palettes/default.yml` | usar sldb directamente | `sldb.notations.builtin_palettes` (`src/sldb/notations/palettes/default.yml`) | `sldb notations list` la lista y su contenido valida igual. |
| SV-H06 | Estilo con una sola precedencia (glifo > `style.kinds` del spec > paleta) | `spec2viz/styling.py` | usar sldb directamente | `sldb.notations.resolve_style`, `sldb.notations.resolve_line_color` | Los casos de precedencia de `tests/test_style_palette.py` pasan contra `sldb.notations`. |

### I. Emparejamiento de átomos con elementos de diagrama

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-I01 | Emparejamiento explícito (`atoms:` en el elemento), alias por título y etiquetas, filtro por tags, avisos y modo estricto (`UnknownAtomError`) | `spec2viz/deskops.py` | migrado a sldb | D4: `sldb.api.matching` (módulos de claves y alias, resolución explícita) | Portados a sldb y en verde: de `tests/test_atoms_matching.py` test_filter_atoms_payload_by_full_tag_or_value; de `tests/test_explicit_atoms.py` test_build_exposes_explicit_map_by_label_and_id, test_unknown_atom_is_warning_unless_strict, test_fully_explicit_view_embeds_no_fuzzy_payload, test_partially_explicit_view_keeps_fuzzy_payload y test_atoms_linked_from_explicit_are_embedded_one_level. IR13b: el catálogo lo usa sin envoltorio (`tests/test_imports.py::test_specir_defines_no_atom_matching_and_no_catalog_path_rule`); los casos de build de `tests/test_explicit_atoms.py` portados en `tests/visual/test_catalog.py` (el desconocido es aviso `matching/unknown-atom`, o `UnknownAtomError` de sldb con `strict_atoms`) y los mismos átomos por elemento que spec2viz en `tests/visual/test_catalog_parity.py` (`test_explicit_atoms_are_spec2viz_s`, `test_strict_atoms_fail_both`). |
| SV-I02 | Emparejamiento difuso de átomos con elementos | `spec2viz/templates/default.html` (en el navegador) | migrado a sldb | D4: `DocumentIndex.rank` sobre `Matcher`/`DifflibMatcher` con alias (sin matcher nuevo); el JS del navegador sigue en SV-G08 | Prueba nueva de D4 de emparejamiento difuso con alias en verde, y SV-G08 cumplida. IR13b: el difuso del navegador es el de la plantilla (SV-G08); el catálogo embebe el mismo payload que spec2viz (`tests/visual/test_catalog_parity.py`). |
| SV-I03 | Referencias `refs: [Model:name]` por elemento hacia documentos sldb y aristas de átomos (`collect_explicit_refs`, `build_explicit_refs`, `attach_atom_edges`) | `spec2viz/deskops.py` | migrado a sldb | D4 (resolución de refs) | `tests/test_refs.py` (14) en verde: los casos de resolución contra sldb (D4) y los de schema y CLI contra specIR (IR12, IR13d). D4 no lista hoy `tests/test_refs.py` entre sus pruebas portadas: ver pendientes. IR13b: las refs de un elemento contra el store de la vista, con sus aristas, iguales a spec2viz en `tests/visual/test_catalog_parity.py` (`test_atoms_of_the_view_s_store_and_its_refs_are_spec2viz_s`, con un store sldb real y una ref desconocida). |
| SV-I04 | Cobertura de átomos por vista | `spec2viz/deskops.py` (`build_coverage_by_view`) | migrado a sldb | D4 (módulo de cobertura) | Prueba de cobertura de D4 en verde y los casos de cobertura de `tests/test_deskops.py` portados. IR13b: la misma `COVERAGE_BY_VIEW` que spec2viz en `tests/visual/test_catalog_parity.py`; el caso de cobertura de `tests/test_deskops.py` portado a través del catálogo en `tests/visual/test_catalog.py`. |
| SV-I05 | Descubrimiento y carga del store de átomos (`SldbAtomResolver`) | `spec2viz/deskops.py` | usar sldb directamente | `sldb.api.stores.open_store` y lectura de documentos y del edge index de `sldb.api` | Las pruebas de SV-I01 a SV-I04 pasan sin `SldbAtomResolver`. IR13b: el catálogo descubre el store de cada vista con `sldb.api.notations.find_store` (con el límite de proyecto de spec2viz) y lee con `StoreReader`; mismo resultado que `SldbAtomResolver` en `tests/visual/test_catalog_parity.py`. |

### J. API Python pública, recursos empaquetados, about y habilidad

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-J01 | `spec2viz.load` y `spec2viz.validate` | `spec2viz/__init__.py` | migrado a sldb | D3: `sldb.api.notations.load_spec`, `validate_spec` | test_load_* (6), test_validate_passes y test_validate_fails de `tests/test_api.py` pasan contra la API de sldb. |
| SV-J02 | `compile_ir`, `render`, `json_schema`, `write_json_schema` | `spec2viz/__init__.py` | migrar tal cual | IR13d (API pública de la capa visual de specIR) | El resto de `tests/test_api.py` (27 en total) portado contra la API de specIR y en verde. IR13d: `specir.visual` exporta `compile_ir`, `render`, `RENDERER_MAP`, `EXT_MAP`, `DEFAULT_RENDERER`, `json_schema` y `write_json_schema` (además, `lint_mermaid`, `assert_mermaid_ok`, `render_catalog`, `build_catalog` y `AnnotationsTarget`); `tests/test_api.py` portado entero en `tests/visual/test_api.py` (27, con `load`/`validate` de sldb, SV-J01) y test_every_public_name_of_spec2viz_has_its_equivalent comprueba cada nombre público del `__init__` de spec2viz. |
| SV-J03 | `render_to_file` con cabecera de procedencia (`with_provenance`, `provenance_header`, `provenance_text`) y salida BPMN doble (`.bpmn` y `.bpmn.html`) | `spec2viz/__init__.py` | migrar tal cual | IR12 lo migra (`src/specir/visual/render_file.py`, lo necesita `diagram render`); IR13d lo expone en la API pública | test_render_to_file_* (7) de `tests/test_api.py` y test_rendered_text_projections_carry_a_provenance_header de `tests/test_cli.py` portados; la cabecera nombra el comando de specIR que valida. IR13d: `render_to_file`, `with_provenance`, `provenance_header` y `provenance_text` en `specir.visual` (`tests/visual/test_api.py`: test_render_to_file_* y test_the_provenance_helpers_name_specir). |
| SV-J04 | Recurso empaquetado: bpmn-js vendorizado | `spec2viz/templates/vendor/bpmn-js/` | migrar tal cual | IR12 (prueba de recursos) | El visor BPMN abre offline (SV-C07) y `tests/test_packaging.py` portado (incluido test_examples_render_successfully) en verde. |
| SV-J05 | Recurso empaquetado: plantilla HTML del catálogo | `spec2viz/templates/default.html` | migrar tal cual | IR12 | Ver SV-G08; la plantilla viaja en el paquete instalado de specIR (prueba de recursos de IR12). |
| SV-J06 | Recursos empaquetados: notaciones y paleta builtin | `spec2viz/notations/`, `spec2viz/palettes/` | usar sldb directamente | Builtins de sldb (`src/sldb/notations/builtin/`, `src/sldb/notations/palettes/`) vía `sldb.notations.builtin_notations` y `builtin_palettes` | specIR no empaqueta notaciones ni paletas; SV-H02 y SV-H05 cumplidas. |
| SV-J07 | Punto de entrada `spec2viz` y empaquetado (instala y arranca) | `pyproject.toml` (`[project.scripts]`), `spec2viz/cli.py` (`main`) | reemplazar | Sustituto: el comando de specIR (IR13d) | Prueba de IR13d: el paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado; test_primary_cli_still_exposes_commands de `tests/test_packaging.py` portado. IR13d: el script `specir` apunta a `specir.cli:main`; `tests/visual/test_packaging.py`: test_primary_cli_still_exposes_commands portado, test_the_script_is_the_command_of_specir_cli y test_the_package_installs_in_a_clean_environment_and_starts_without_spec2viz (venv nuevo con sldb y la wheel de specIR, sin spec2viz: `specir --help`, `about`, `render` y `validate` arrancan e `import spec2viz` falla). |
| SV-J08 | Comando about (dónde viven los diagramas y cómo llega el flujo al HTML) | `spec2viz/cli.py` (`about`) | migrar tal cual | IR13d | El comando equivalente de specIR existe y lo invoca la prueba de CLI de IR13d; su texto nombra los comandos de specIR y de sldb que sustituyen a los de spec2viz. IR13d: `specir about` (store sobre el directorio actual, flujo a HTML con los comandos de specIR y los de sldb para el store y las anotaciones); test_about_names_the_commands_of_specir_and_sldb (invoca con `--help` cada comando que nombra) y test_about_shows_the_store_above_the_current_directory de `tests/visual/test_cli.py`. |
| SV-J09 | Habilidad de agente use-spec2viz | `.pi/skills/use-spec2viz/SKILL.md` (copia distinta en `deskops/.opencode/skills/use-spec2viz/SKILL.md`) | reemplazar | Sustituto: `skills/use-specir/SKILL.md` (IR13d) | Prueba de IR13d que extrae los comandos que nombra la habilidad y los invoca con ayuda; la habilidad no nombra comandos de spec2viz. IR13d: `skills/use-specir/SKILL.md`; test_the_skill_names_only_commands_that_exist (extrae los `specir …` y `sldb …` de la habilidad y los invoca con `--help`, con sus opciones) y test_the_skill_names_no_spec2viz_command de `tests/visual/test_cli.py`. |

### K. Comandos y subgrupos del CLI

Una fila por cada entrada que lista la ayuda (`spec2viz --help` y la de cada subgrupo). La correspondencia
detallada la escribe IR13d en `docs/spec2viz/correspondencia-cli.md`. Cuando la capacidad vive en sldb, el
equivalente es el comando de sldb y specIR no define subcomando propio.

| ID | Comando | Modo | Equivalente | Condición de retiro |
|---|---|---|---|---|
| SV-K01 | `spec2viz about` | migrar tal cual | Comando about de specIR (IR13d) | SV-J08. IR13d: `specir about`; test_about_names_the_commands_of_specir_and_sldb. |
| SV-K02 | `spec2viz build` (alias de `catalog build`) | migrar tal cual | Alias en el comando de specIR (IR13d) | SV-G01; test_catalog_build_alias_matches_legacy_build portado. IR13d: `specir build`; test_catalog_build_alias_matches_legacy_build y test_build_command* de `tests/visual/test_cli.py`. |
| SV-K03 | `spec2viz catalog` (subgrupo) | migrar tal cual | Subgrupo catalog de specIR con build y schema; sync, validate y serve remiten a sldb | SV-K04 a SV-K08 cumplidas. IR13d: `specir catalog` (build, schema); test_help_mentions_taxonomy_groups_and_renderers y test_specir_defines_no_command_the_table_gives_to_sldb de `tests/visual/test_cli.py`. |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | specIR (IR13b, IR13d) | SV-G01. IR13d: `specir catalog build` (con `--annotations`, `--sldb-url` y `--annotations-doc`); test_build_command_extracts_* y test_catalog_build_embeds_the_annotations_saver_of_ir13b de `tests/visual/test_cli.py`. |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A16. IR13d: `specir catalog schema`; test_catalog_schema_stdout de `tests/visual/test_cli.py`. |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve` sobre el store del catálogo (IR13b) | SV-G06. IR13d: `sldb serve --store --cors`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` (D1) | SV-G04. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` (D1) | SV-G05. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K09 | `spec2viz diagram` (subgrupo) | migrar tal cual | Subgrupo diagram de specIR con render, lint y schema (y validate, ver SV-K16); sync, from-graph y generate remiten a sldb | SV-K10 a SV-K16 cumplidas. IR13d: `specir diagram` (render, validate, lint, schema); test_help_mentions_taxonomy_groups_and_renderers de `tests/visual/test_cli.py`. |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot/--store` (D2) | SV-F01; test_cli_from_graph_* (5) y test_cli_from_graph_module_prefix reescritos contra el comando de sldb (D2). IR13d: `sldb notations from-graph --snapshot/--store`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python` (D2) | SV-F02. IR13d: `sldb notations from-graph --python`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | specIR (IR12, IR13d) | SV-D01. IR13d: `specir diagram lint`; test_lint_alias_matches_diagram_lint de `tests/visual/test_cli.py`. |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | specIR (IR12, IR13d) | test_render_* de `tests/test_cli.py` portados; SV-C01 a SV-C12. IR13d: `specir diagram render`; test_render_* de `tests/visual/test_render_commands.py` (IR12) y test_the_render_alias_writes_what_diagram_render_writes de `tests/visual/test_cli.py`. |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A15. IR13d: `specir diagram schema`; `tests/visual/test_schema.py` (IR12) y test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec` (D1) | SV-E01. IR13d: `sldb notations sync --spec`; test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb | Lógica en sldb (`load_spec`, `validate_spec`, D3). Decisión de IR13d: sldb aún no tiene comando que valide un spec (pedido en su inbox; `sldb validate` valida contra un modelo, sin despacho por tipo ni validación semántica), así que `specir diagram validate` y el alias `specir validate` quedan en specIR de forma provisional: solo llaman a `load_spec` y `validate_spec` de sldb, sin redefinir nada. Cuando sldb publique su comando, los de specIR se retiran, la cabecera de procedencia lo nombra y la fila pasa a «usar sldb directamente» (`docs/spec2viz/correspondencia-cli.md`) | test_validate_valid, test_validate_invalid y test_validate_all_types de `tests/test_cli.py` portados contra el comando elegido; SV-A11 y SV-A12. IR13d: test_validate_valid, test_validate_invalid y test_validate_all_types portados sobre `specir validate`, y test_diagram_validate_valid y test_diagram_validate_invalid sobre `specir diagram validate`, en `tests/visual/test_cli.py`. |
| SV-K17 | `spec2viz lint` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K12. IR13d: `specir lint`; test_lint_alias_matches_diagram_lint y test_every_alias_stands_for_a_group_command_with_the_same_parameters de `tests/visual/test_cli.py`. |
| SV-K18 | `spec2viz notation` (subgrupo) | usar sldb directamente | `sldb notations` | SV-K19 a SV-K22 cumplidas. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`); specIR no define el subgrupo (test_specir_defines_no_command_the_table_gives_to_sldb). IR13g: SV-K19, SV-K20 y SV-K22 cumplidas; sigue abierta por SV-K21. |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | SV-H02. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | SV-E02. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation`; sldb no tiene hoy comando de validación de notaciones (ver pendientes) | SV-H01 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. IR13d: la tabla remite a `sldb.notations.load_notation`, que test_every_equivalent_of_the_table_answers_its_help invoca sobre cada builtin; el comando de sldb sigue pedido. |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view` | SV-H03. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). IR13g: SV-H03 cumplida. |
| SV-K23 | `spec2viz palette` (subgrupo) | usar sldb directamente | `sldb notations` (`list`, `sync --palette`) | SV-K24 a SV-K26 cumplidas. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`); specIR no define el subgrupo. |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` (incluye `builtin_palettes`) | SV-H05. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | SV-E02. IR13d: test_every_equivalent_of_the_table_answers_its_help de `tests/visual/test_cli.py` lo invoca con `--help` (`docs/spec2viz/correspondencia-cli.md`). |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (con contraste WCAG); sldb no tiene hoy comando de validación de paletas (ver pendientes) | SV-H04 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. IR13d: la tabla remite a `sldb.notations.load_palette`, que test_every_equivalent_of_the_table_answers_its_help invoca sobre cada builtin; el comando de sldb sigue pedido. |
| SV-K27 | `spec2viz render` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K13. IR13d: `specir render`; test_render_each_type (6), test_render_override, test_render_backend_alias, test_render_multiple, test_render_invalid_fails, test_render_d2, test_render_antonia_html y test_render_json_reflection_artifact portados sobre el alias en `tests/visual/test_cli.py`. |
| SV-K28 | `spec2viz schema` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K14. IR13d: `specir schema`; test_schema_stdout, test_schema_outfile, test_schema_diagram_store_stdout y test_schema_invalid_type_fails de `tests/visual/test_cli.py`. |
| SV-K29 | `spec2viz validate` (alias) | migrado a sldb | Igual que SV-K16 | SV-K16. IR13d: `specir validate`; ver SV-K16. |
| SV-K30 | Ayuda raíz con taxonomía (diagram, catalog) y lista de renderers | migrar tal cual | Ayuda del comando de specIR (IR13d) | test_help_mentions_taxonomy_groups_and_renderers de `tests/test_cli.py` portado. IR13d: test_help_mentions_taxonomy_groups_and_renderers portado en `tests/visual/test_cli.py`; la ayuda dice «Top-level aliases (render, validate, lint, schema, build) remain available» donde spec2viz decía «Legacy top-level commands remain available». |

### Pruebas de spec2viz por fila

Cada archivo de `spec2viz/tests/` y las filas que lo portan o reemplazan. El gate G2 exige que cada
archivo tenga todos sus casos cubiertos por alguna fila.

| Archivo | Filas |
|---|---|
| `tests/test_activity_lanes.py` | SV-A05, SV-B07, SV-C02, SV-C03, SV-C04 |
| `tests/test_api.py` | SV-A15, SV-B02, SV-C01, SV-C05, SV-C10, SV-J01, SV-J02, SV-J03 |
| `tests/test_atoms_matching.py` | SV-G07, SV-G08, SV-I01, SV-I02 |
| `tests/test_base_model.py` | SV-A09 |
| `tests/test_bpmn.py` | SV-C06, SV-C07, SV-C08, SV-J03 |
| `tests/test_catalog_notation.py` | SV-G04, SV-G05 |
| `tests/test_catalog_paths.py` | SV-G02 |
| `tests/test_catalog_resolved_views.py` | SV-C14, SV-G03 |
| `tests/test_class_diagram.py` | SV-A01, SV-B03, SV-C13 |
| `tests/test_class_packages.py` | SV-A01, SV-B03, SV-C13 |
| `tests/test_cli.py` | SV-A15, SV-A16, SV-C01, SV-C04, SV-C11, SV-C12, SV-G01, SV-J03, SV-K01 a SV-K30 |
| `tests/test_compilers.py` | SV-B02 a SV-B09 |
| `tests/test_deployment_nested.py` | SV-A06, SV-B08, SV-C02, SV-C03, SV-C04 |
| `tests/test_deskops.py` | SV-G07, SV-I04 |
| `tests/test_exceptions.py` | SV-A13, SV-A14 |
| `tests/test_explicit_atoms.py` | SV-I01 |
| `tests/test_graph_import.py` | SV-F01, SV-K10 |
| `tests/test_ir.py` | SV-B01 |
| `tests/test_loader.py` | SV-A11 |
| `tests/test_mermaid_mmdc.py` | SV-D01 |
| `tests/test_models_activity.py` | SV-A05 |
| `tests/test_models_component.py` | SV-A04 |
| `tests/test_models_deployment.py` | SV-A06 |
| `tests/test_models_matrix.py` | SV-A07 |
| `tests/test_models_sequence.py` | SV-A02 |
| `tests/test_models_state.py` | SV-A03 |
| `tests/test_notation.py` | SV-H01, SV-H02 |
| `tests/test_notation_view.py` | SV-H03 |
| `tests/test_packaging.py` | SV-A15, SV-J04, SV-J07 |
| `tests/test_reflection_compiler.py` | SV-B10 |
| `tests/test_refs.py` | SV-I03 |
| `tests/test_renderers.py` | SV-C02 a SV-C11, SV-C13 |
| `tests/test_rendering_bug.py` | SV-C15 |
| `tests/test_sldb_sync.py` | SV-E01, SV-E02 |
| `tests/test_style_palette.py` | SV-E02, SV-H04, SV-H06 |
| `tests/test_validator.py` | SV-A12 |
| `tests/test_view_contract_resolved.py` | SV-H03 |
| `tests/test_view_doc.py` | SV-A17 |

## Inventario de consumidores

Universo auditado por IR13 (y solo este; añadir uno exige actualizar primero esta sección). Búsqueda hecha
el 2026-11-15 sobre los repos con `.git` bajo `SLDB_1/` (`IR`, `deskops`, `pron`, `scion`, `sldb`,
`spec2viz`, `UIs/graph_ui`; `sldb-runtime` y `deskops-runtime` son checkouts de despliegue de `sldb` y
`deskops` y se auditan por su repo de origen) y sobre todo `store.yaml` y `store_index.yaml` bajo
`SLDB_1/`. `scion` no tiene dependencias de spec2viz. Clases de dependencia como las define IR13
(importación, dependencia declarada, invocación del comando, modelo registrado en un store).

| Consumidor | Archivo y línea | Clase | Sustituto previsto |
|---|---|---|---|
| graph_ui | `UIs/graph_ui/frontends/mindmap/sldb_adapter.py:245` (`from spec2viz.notation_view import ViewError, resolve_view`) | importación | `sldb.api.notations.resolve_view` y `ViewError` (SV-H03) |
| graph_ui | `UIs/graph_ui/frontends/mindmap/sldb_adapter.py:437` (`from spec2viz.notation_view import ViewError, resolve_documents`) | importación | `sldb.api.notations.resolve_documents` (SV-H03) |
| graph_ui | `UIs/graph_ui/pyproject.toml:19` (extra `notation = ["spec2viz>=0.1.0"]`) y `:24` (extra `test`) | dependencia declarada | quitar; sldb ya es dependencia |
| graph_ui | `UIs/graph_ui/.github/requirements-suite.txt:10` (`-e git+https://github.com/jpcosec/spec2viz@master#egg=spec2viz`, lo usa el CI para leer los specs piloto) | dependencia declarada (CI) | specs piloto copiados como fixtures o leídos desde specIR |
| graph_ui | `UIs/graph_ui/tests/test_projection_views.py:18` (importorskip), `:33` y `:82` (`spec2viz diagram sync`), `:167` (`spec2viz.sldb_models` ViewDoc) | importación e invocación | `sldb notations sync --spec` (SV-E01), `ViewDoc` de sldb (SV-A17) |
| graph_ui | `UIs/graph_ui/tests/test_mindmap_notation.py:20-21` (`from spec2viz.notation_view import resolve_view`) y `:45` (`spec2viz diagram sync`) | importación e invocación | SV-H03, SV-E01 |
| graph_ui | `UIs/graph_ui/tests/e2e_notation_class.py:58`, `e2e_notation_sequence.py:108`, `e2e_notation_deployment.py:92`, `e2e_notation_activity.py:128`, `e2e_notation_style.py:147`, `e2e_notation_legibility.py:38` y `:175`, `e2e_mindmap_notation.py:27` y `:48`, `e2e_review_workbench_views.py:40`, `:76` y `:96` (`spec2viz diagram sync` e importorskip) | importación e invocación | SV-E01 |
| deskops | `deskops/deskops/graph/desk_graph.py:75` (regla de rutas `FileRule(kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"))`) | regla de rutas del grafo del desk | (†) decidido (coordinador, aceptado por JP el 2026-11-15): la regla deja de nombrar spec2viz y reconoce los specs YAML como artefactos de autoría sincronizados con `sldb notations sync`; lo hace el desk de deskops |
| deskops | `deskops/desk/drawer/plans/workspace-documental/render_diagram.py:7` y `:9` (`spec2viz diagram validate` y `diagram render`) | invocación | comandos de specIR (SV-K13, SV-K16) |
| deskops | `deskops/docs/diagrams/README.md` y los `.md`/`.mmd` de `deskops/docs/diagrams/` que nombran a spec2viz | documentación de diagramas (no cuenta como dependencia para IR13; se regenera con specIR) | renderers de specIR |
| deskops | `deskops/.opencode/skills/use-spec2viz/SKILL.md`; `deskops/.claude/skills/deskops-workflow/SKILL.md` y `references/spec2viz-cli.md` (instruyen a agentes a invocar `spec2viz`) | habilidad de agente | `skills/use-specir/SKILL.md` (SV-J09) |
| pron | `pron/docs/spec2viz/build.py:22-24` (`spec2viz diagram validate`, `diagram render --backend mermaid`, `catalog build`) | invocación | comandos de specIR (SV-K13, SV-K16, SV-K04) |
| sldb | `sldb/docs/architecture/spec2viz/vistas.yml` y sus specs (`current-*.yml`, `python-ast.yml`) | registro de catálogo que construye `spec2viz catalog build` | decidido (coordinador, aceptado por JP el 2026-11-15): los specs se quedan como fixtures durante la paridad; el catálogo se construye con `specir catalog build` (SV-G01) y se sincroniza con `sldb notations sync --catalog`; lo hace el desk de sldb |
| sldb | `sldb/contracts/identity.toml:299` (`consumers = [..., "spec2viz", ...]`) | configuración de contrato | quitar spec2viz de la lista al retirarlo |
| IR (specIR) | `IR/tests/conftest.py:24` y `:80` (federa el store `spec2viz/.sldb`), `IR/tests/test_mcp_extension.py:24` (`SPEC_STORE = "spec2viz"`) | lectura del store de spec2viz en pruebas | store con modelos de sldb (G5) o fixture propio |
| store `spec2viz/.sldb` | `spec2viz/.sldb/store.yaml:44-57`, `spec2viz/.sldb/core/store_index.yaml:141-194`, `spec2viz/.sldb/core/models/{SpecDoc,SpecNodeDoc,NotationDoc,GlyphDoc,LinkDoc,PaletteDoc,ViewDoc}.yaml` | modelos `spec2viz.sldb_models` registrados | `sldb.models.notation.*` (SV-A17) |

Es el único store bajo `SLDB_1/` cuyo índice registra `spec2viz.sldb_models`.

Specs YAML existentes que afecta la decisión del YAML (†): `spec2viz` (44: `tests/fixtures/`,
`docs/architecture/spec2viz/`, `examples/`), `sldb` (46: `tests/fixtures/`, `docs/architecture/`),
`UIs/graph_ui` (24: `tests/fixtures/`, `docs/representacion/`), `pron` (4: `docs/spec2viz/specs/`),
`deskops` (1: `desk/drawer/plans/workspace-documental/`). Conteo de archivos con `type:` de uno de los
ocho tipos en la raíz, sin `.sldb/`, `build/` ni entornos. Alineados con la decisión aceptada (G7): se
quedan donde están; durante la paridad son fixtures y después cada repo decide por su desk.

## Pendientes de derivación

Lo que esta matriz deja abierto y debe convertirse en tarea o pedido (no lo resuelve IR07):

1. Filas «usar sldb directamente» (SV-A17, SV-E02, SV-H01 a SV-H06, SV-I05, SV-J06, SV-K18 a SV-K26):
   con IR13c retirada, ninguna tarea porta hoy `tests/test_notation.py`, `tests/test_notation_view.py`,
   `tests/test_view_contract_resolved.py`, `tests/test_style_palette.py` ni `tests/test_view_doc.py`
   contra sldb. La prueba de paridad la aporta IR13 (prueba en specIR que llama a sldb sin envoltorio) o
   una tarea nueva derivada de estas filas.
2. SV-K21 y SV-K26: sldb no tiene comando para validar una notación o una paleta por nombre o ruta.
   Pedido al desk de sldb en la nota `20261115-192054` (la misma que pide validar un spec, SV-K16); sigue
   abierto.
3. SV-K16 y SV-K29: decidido en IR13d. Mientras sldb no tenga el comando (pedido a su desk), lo da
   `specir diagram validate` (y `specir validate`) sobre `load_spec`/`validate_spec` de sldb, sin redefinir
   nada; se retira cuando sldb lo publique.
4. SV-I03: resuelto. sldb portó los 9 casos de resolución y aristas en `tests/matching/test_matching_refs.py`
   (D4) e IR13 portó los 3 de modelos y schema en `tests/visual/test_refs_models.py`.
5. SV-C13 y SV-C14: resuelto por IR12, que incluyó en su lista de archivos los backends UML de clases y el
   mermaid desde vista resuelta.
6. Consumidores: IR13 envió los pedidos de migración a los desks de deskops, graph_ui, pron, sldb y
   spec2viz (store); las notas y su estado están en `docs/spec2viz/acta-de-retiro.md`.
7. Filas con pruebas de mmdc (SV-B03, SV-C13, SV-C14, SV-D01, SV-G03 y, por dependencia, SV-K09, SV-K12 y
   SV-K17): resuelto el 2026-11-15 con mermaid-cli 12.2 sobre Chrome headless
   (`SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc`, ver «Acreditación (IR13)»). SV-K09 sigue
   abierta por SV-K16.
8. Exporter de BPMN y clave de `localStorage` del catálogo (SV-C06, SV-G06): decidido por el coordinador y
   aceptado por JP. Mientras dure la paridad se mantienen `exporter="spec2viz"`,
   `targetNamespace="http://spec2viz/bpmn"` y la clave `spec2viz.catalog.annotations.v1`; en el momento
   del retiro pasan a specir con goldens nuevos y migración de anotaciones (paso del acta de retiro).

## Acreditación (IR13)

Evaluada por IR13 el 2026-11-15 sobre IR `dc5496a` y sldb `d4aeb4b1`, cada archivo de pruebas corrido por
separado con `TMPDIR=/dev/shm` (las de sldb con el entorno de IR, que instala sldb editable desde
`sldb/src`). Una fila es **cumplida** solo si su condición de retiro se cumple entera y la prueba citada
pasa; si depende de otra fila abierta, queda abierta. `specir retirement check` exige que cada fila esté
cumplida y cite al menos una prueba (`tests/….py`). Resumen: 96 cumplidas, 9 abiertas (tras IR13g); el detalle
por gate y por consumidor está en `docs/spec2viz/acta-de-retiro.md`.

Corrida con motor real de mermaid (2026-11-15, decisiones de JP): `@mermaid-js/mermaid-cli` instalado en
`/mnt/ssd/herramientas/mermaid-cli` con el Chrome del sistema en headless (envoltorio `mmdc` de ese
directorio) y `SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc`. Ningún caso de mmdc se salta:
`tests/visual/test_lint_mermaid.py` 15 passed (antes 8 passed, 7 skipped), `tests/visual/test_render_cases.py`
30 passed (antes 27 passed, 3 skipped; se arregló que dos casos llamaban a `mmdc` del PATH en lugar de
`mmdc_path()`), `tests/visual/test_render_parity.py` 82 passed. El motor real rechazaba los ids con guion de
la proyección de estados (`[*] --> post-draft`): el renderer mermaid de estados escribe ahora ids con solo
letras, dígitos y `_` (`post_draft`), sin tocar los que ya lo eran (la paridad con spec2viz no cambia); el
pseudoestado `*` (`__any_state`) lo acepta el motor. Con eso pasan a cumplidas SV-B03, SV-C13, SV-C14,
SV-D01, SV-G03, SV-K12 y SV-K17; SV-K09 sigue abierta por SV-K16.

IR13e (`task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`,
2026-11-16, sldb `9307d485`, spec2viz `b624b75`): `tests/visual/test_notations_parity.py` corre contra
sldb, sin importar spec2viz, 42 pruebas portadas de `tests/test_view_doc.py` (3), `test_notation.py` (12
de 14), `test_notation_view.py` (10 de 11), `test_view_contract_resolved.py` (2) y `test_style_palette.py`
(15 de 16), más 9 comparaciones «valida igual» (8 notaciones y la paleta `default` copiadas en
`tests/visual/fixtures/spec2viz-notations/`, `model_dump()` igual al de la builtin de sldb): 51 pruebas,
88 passed, 1 xfailed (89 casos parametrizados). Las 6 pruebas de spec2viz que invocan su CLI no se portan
enteras: su parte de CLI es de las filas K (`tests/visual/test_cli.py`); la validación tipada sin CLI de
dos de ellas sí se porta (ciclo de corrección 1): test_notation_load_gives_typed_errors (7 casos, de
test_notation_validate_gives_typed_errors, en SV-H01) y test_palette_check_is_typed (6 casos, de
test_palette_validation_is_typed, en SV-H04). Pasan a cumplidas SV-E02, SV-H02, SV-H04, SV-H05, SV-H06,
SV-J06, SV-K19, SV-K20, SV-K24 y SV-K25, y también SV-G08 y SV-I02 (sldb arregló `label_key` con `_` en
`06dbcf02` y el xfail de `tests/visual/test_catalog.py` se quitó en `4dc8946`). Siguen abiertas SV-A17
(solo G5), SV-H01 (un caso xfail estricto, nota a sldb 20261116-022332), SV-H03 (solo G4 de graph_ui),
SV-K18, SV-K22 y SV-K23.

IR13g (`task-ir13g-acreditar-en-la-matriz-y-el-acta-que-graph-ui-ya-no-depende-de-spec2viz-79d63ee`,
2026-11-16, IR `3ec37f2`, sldb `b0e4f649`, graph_ui `824c135`): graph_ui avisó (nota de inbox de IR
20261116-131509) que su master `79d63ee` (closeout `c9b09f7`) ya no depende de spec2viz. Comprobado desde
IR: `git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD` rc 0; `git grep -nE 'from spec2viz|import
spec2viz|spec2viz>=' HEAD` no encuentra nada fuera de `desk/` y `runs/` (solo notas y evidencia), ni en
`pyproject.toml` ni en `.github/requirements-suite.txt`; `specir retirement check` no lista dependencias
de graph_ui. `tests/visual/test_notations_parity.py` sale con 88 passed, 1 xfailed (el de mindmap de
SV-H01); las 13 pruebas de SV-H03 (19 casos) pasan sin xfail. Pasan a cumplidas SV-H03 y SV-K22. SV-K18
sigue abierta: depende de SV-K21.

| Fila | Estado | Prueba que la acredita | Falta |
|---|---|---|---|
| `SV-A01` | cumplida | sldb `tests/notations/test_spec_class_diagram.py` (17 passed) y `tests/notations/test_spec_class_packages.py` (7 passed), con los seis casos nombrados; IR `tests/visual/test_visual_names.py` (4 passed): specIR no define el modelo. | - |
| `SV-A02` | cumplida | sldb `tests/notations/test_spec_models_sequence.py` (3 passed); IR `tests/visual/test_visual_names.py` (4 passed). | - |
| `SV-A03` | cumplida | sldb `tests/notations/test_spec_models_state.py` (3 passed); IR `tests/visual/test_visual_names.py`. | - |
| `SV-A04` | cumplida | sldb `tests/notations/test_spec_models_component.py` (3 passed); IR `tests/visual/test_visual_names.py`. | - |
| `SV-A05` | cumplida | sldb `tests/notations/test_spec_models_activity.py` (3 passed); IR `tests/visual/test_visual_names.py`. | - |
| `SV-A06` | cumplida | sldb `tests/notations/test_spec_models_deployment.py` (4 passed); IR `tests/visual/test_visual_names.py`. | - |
| `SV-A07` | cumplida | sldb `tests/notations/test_spec_models_matrix.py` (4 passed); IR `tests/visual/test_visual_names.py`. | - |
| `SV-A08` | cumplida | IR `tests/visual/test_visual_parity.py` (90 passed): sldb y spec2viz dan el mismo error (clase y texto) sobre los 44 specs del corpus, `examples/reflection/` incluido. | - |
| `SV-A09` | cumplida | sldb `tests/notations/test_spec_base_model.py` (3 passed). | - |
| `SV-A10` | cumplida | IR `tests/visual/test_catalog_parity.py` (29 passed: `check_catalog` y la página sobre `examples/catalog/` y `docs/architecture/vistas.yml` iguales a spec2viz) y `tests/visual/test_catalog.py` (67 passed). | - |
| `SV-A11` | cumplida | sldb `tests/notations/test_spec_loader.py` (20 passed, incluye los 16 de spec2viz). | - |
| `SV-A12` | cumplida | sldb `tests/notations/test_spec_validator.py` (19 passed). | - |
| `SV-A13` | cumplida | sldb `tests/notations/test_spec_exceptions.py` (2 passed). | - |
| `SV-A14` | cumplida | IR `tests/visual/test_visual_compilers.py` (28 passed, `CompileError`/`Spec2VizError`), `tests/visual/test_renderers.py` (56 passed) y `tests/visual/test_bpmn.py` (26 passed, `RenderError`). | - |
| `SV-A15` | cumplida | IR `tests/visual/test_schema.py` (13 passed), `tests/visual/test_api.py` (31 passed), `tests/visual/test_cli.py` (44 passed). | - |
| `SV-A16` | cumplida | IR `tests/visual/test_cli.py` (test_schema_diagram_store_stdout, test_catalog_schema_stdout). | - |
| `SV-A17` | abierta | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_defaults_and_shape, test_invalid y test_view_doc_in_a_store_references_its_notation, con `ViewDoc` de `sldb.api`. | Solo G5: `spec2viz/.sldb` registra `spec2viz.sldb_models` (pedido al desk de spec2viz, nota 20261115-225013; fuera de IR13e). |
| `SV-B01` | cumplida | IR `tests/visual/test_visual_ir.py` (3 passed). | - |
| `SV-B02` | cumplida | IR `tests/visual/test_visual_compilers.py` (28 passed), `tests/visual/test_api.py` (31 passed) y `tests/visual/test_visual_parity.py` (90 passed). | - |
| `SV-B03` | cumplida | IR `tests/visual/test_visual_compilers.py` (28 passed) y `tests/visual/test_render_cases.py` (30 passed, 0 skipped con `SPECIR_MMDC` apuntando a mermaid-cli real: test_real_mermaid_engine_accepts_members_kinds_and_all_relations y test_real_mermaid_engine_accepts_the_packages en verde). | - |
| `SV-B04` | cumplida | IR `tests/visual/test_visual_compilers.py` (28 passed) y `tests/visual/test_visual_parity.py` (90 passed). | - |
| `SV-B05` | cumplida | IR `tests/visual/test_visual_compilers.py` y `tests/visual/test_visual_parity.py`. | - |
| `SV-B06` | cumplida | IR `tests/visual/test_visual_compilers.py` y `tests/visual/test_visual_parity.py`. | - |
| `SV-B07` | cumplida | IR `tests/visual/test_visual_compilers.py`, `tests/visual/test_render_cases.py` (carriles de actividad) y `tests/visual/test_visual_parity.py`. | - |
| `SV-B08` | cumplida | IR `tests/visual/test_visual_compilers.py`, `tests/visual/test_render_cases.py` (despliegue anidado) y `tests/visual/test_visual_parity.py`. | - |
| `SV-B09` | cumplida | IR `tests/visual/test_visual_compilers.py` y `tests/visual/test_visual_parity.py`. | - |
| `SV-B10` | cumplida | IR `tests/visual/test_visual_compilers.py` (test_reflection_*). | - |
| `SV-C01` | cumplida | IR `tests/visual/test_api.py` (31 passed), `tests/visual/test_cli.py` (44 passed), `tests/visual/test_render_commands.py` (33 passed). | - |
| `SV-C02` | cumplida | IR `tests/visual/test_renderers.py` (56 passed), `tests/visual/test_render_parity.py` (81 passed), `tests/visual/test_render_cases.py` (27 passed). | - |
| `SV-C03` | cumplida | IR `tests/visual/test_renderers.py`, `tests/visual/test_render_parity.py`, `tests/visual/test_render_cases.py`. | - |
| `SV-C04` | cumplida | IR `tests/visual/test_renderers.py`, `tests/visual/test_render_parity.py`, `tests/visual/test_render_cases.py`, `tests/visual/test_cli.py` (test_render_d2). | - |
| `SV-C05` | cumplida | IR `tests/visual/test_renderers.py`, `tests/visual/test_render_parity.py` (escala `kindColor` como correspondencia), `tests/visual/test_api.py` (test_render_to_file_vega). | - |
| `SV-C06` | cumplida | IR `tests/visual/test_bpmn.py` (26 passed). Decisión (coordinador, aceptada por JP el 2026-11-15): mientras dure la paridad el XML mantiene `exporter="spec2viz"` y `targetNamespace="http://spec2viz/bpmn"`; al retirar spec2viz pasan a specir con goldens nuevos (paso del acta). | - |
| `SV-C07` | cumplida | IR `tests/visual/test_bpmn.py` y `tests/visual/test_resources.py` (7 passed). | - |
| `SV-C08` | cumplida | IR `tests/visual/test_bpmn.py`. | - |
| `SV-C09` | cumplida | IR `tests/visual/test_renderers.py`. | - |
| `SV-C10` | cumplida | IR `tests/visual/test_renderers.py`, `tests/visual/test_api.py` y `tests/visual/test_resources.py`. | - |
| `SV-C11` | cumplida | IR `tests/visual/test_renderers.py` y `tests/visual/test_cli.py` (test_render_antonia_html). | - |
| `SV-C12` | cumplida | IR `tests/visual/test_cli.py` y `tests/visual/test_render_commands.py` (test_render_json_reflection_artifact). | - |
| `SV-C13` | cumplida | IR `tests/visual/test_renderers.py` (56 passed) y `tests/visual/test_render_cases.py` (30 passed, 0 skipped con `SPECIR_MMDC` apuntando a mermaid-cli real: los casos de clases con el motor real en verde). | - |
| `SV-C14` | cumplida | IR `tests/visual/test_render_cases.py` (30 passed, 0 skipped con `SPECIR_MMDC` apuntando a mermaid-cli real: test_view_to_mermaid_is_accepted_by_the_real_engine y test_view_to_mermaid_matches_spec2viz_on_the_same_resolved_view en verde; los 4 casos `view_to_mermaid` de `tests/test_catalog_resolved_views.py`) y `tests/visual/test_catalog.py` (sus casos de `catalog build`). | - |
| `SV-C15` | cumplida | IR `tests/visual/test_render_commands.py` (caso de `tests/test_rendering_bug.py`). | - |
| `SV-D01` | cumplida | IR `tests/visual/test_lint_mermaid.py` (15 passed, 0 skipped con `SPECIR_MMDC` apuntando a mermaid-cli real: los 4 casos de `tests/test_mermaid_mmdc.py` y los demás de mmdc en verde) y `tests/visual/test_render_parity.py` (82 passed con mmdc, incluido el render de la proyección de estados con ids con guion). | - |
| `SV-E01` | cumplida | sldb `tests/notations/test_spec_sync.py` (16 passed); IR `tests/visual/test_sync_generation_parity.py` (22 passed). | - |
| `SV-E02` | cumplida | sldb `tests/notations/test_spec_sync.py` (casos de notación y paleta de `tests/test_sldb_sync.py`); IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_notation_sync_writes_docs_and_edges, test_notation_sync_is_idempotent_and_prunes, test_notation_naming_an_unregistered_model_is_reported, test_wildcard_link_leaves_no_dangling_relation_type, test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend y test_unstyled_notation_writes_no_palette_and_no_style, contra `NotationSync`/`SpecSync` de `sldb.api.notations` y store real. | - |
| `SV-F01` | cumplida | sldb `tests/notations/test_component_spec_graph.py` (16 passed) y `tests/notations/test_notations_from_graph_cli.py` (6 passed); IR `tests/visual/test_sync_generation_parity.py` (22 passed). | - |
| `SV-F02` | cumplida | sldb `tests/notations/test_component_spec_python.py` (4 passed); IR `tests/visual/test_sync_generation_parity.py`. Diferencia declarada; la pérdida de imports anidados sigue pedida a sldb (nota 20261115-203456). | - |
| `SV-G01` | cumplida | IR `tests/visual/test_catalog.py` (67 passed), `tests/visual/test_catalog_parity.py` (29 passed), `tests/visual/test_cli.py` (44 passed). | - |
| `SV-G02` | cumplida | IR `tests/visual/test_catalog.py` (los 9 de `tests/test_catalog_paths.py`). | - |
| `SV-G03` | cumplida | IR `tests/visual/test_catalog.py` (68 passed con `SPECIR_MMDC` apuntando a mermaid-cli real), `tests/visual/test_catalog_parity.py` y `tests/visual/test_render_cases.py` (caso con el motor real de `tests/test_catalog_resolved_views.py` en verde, compartido con SV-C14). | - |
| `SV-G04` | cumplida | sldb `tests/notations/test_spec_catalog_sync.py` (8 passed); IR `tests/visual/test_catalog_parity.py` y `tests/visual/test_catalog.py`. | - |
| `SV-G05` | cumplida | sldb `tests/notations/test_spec_catalog_sync.py`; IR `tests/visual/test_catalog_parity.py`. | - |
| `SV-G06` | cumplida | IR `tests/visual/test_catalog_annotations.py` (5 passed, con `sldb serve --cors` real). Decisión (coordinador, aceptada por JP el 2026-11-15): la página mantiene la clave `spec2viz.catalog.annotations.v1` de `localStorage` mientras dure la paridad; al retirar spec2viz pasa a una clave de specir con migración de las anotaciones guardadas (paso del acta). | - |
| `SV-G07` | cumplida | IR `tests/visual/test_catalog.py` y `tests/visual/test_catalog_parity.py`. | - |
| `SV-G08` | cumplida | IR `tests/visual/test_catalog.py` (68 passed, sin xfailed ni xpassed con `SPECIR_MMDC` apuntando a mermaid-cli real): los casos de emparejamiento en el navegador, de markdown de átomos y test_tabs_follow_the_target_atom, y test_label_key_of_sldb_is_the_template_s_norm_key y test_label_key_of_sldb_splits_underscores_like_norm_key sin xfail (sldb arregló `label_key` con `_` en `06dbcf02`, nota 20261115-214942; el xfail se quitó en `4dc8946`). | - |
| `SV-H01` | abierta | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_builtins_load_and_cover_every_diagram_type, test_wildcard_link_and_free_relations, test_uml_class_notation_matches_the_class_spec_vocabulary, test_statechart_nests_contains_and_marks_the_initial_state, test_minimal_notation_defaults, test_free_relation_diagram_types_accept_any_relation, test_load_notation_from_path_and_unknown_name y test_notation_load_gives_typed_errors (7 casos: parte no CLI de test_notation_validate_gives_typed_errors de `tests/test_style_palette.py`, errores tipados de `load_notation` de sldb) pasan; test_invalid_notations_are_rejected pasa en 14 de sus 15 casos. Los 2 casos CLI de `tests/test_notation.py` son de las filas K. | xfail estricto test_invalid_notations_are_rejected[changes1-not a spec2viz diagram type]: sldb rechaza `diagram_type: mindmap` con «diagram_type 'mindmap' is not a valid diagram type» donde spec2viz decía «not a spec2viz diagram type»; pedido a sldb (nota 20261116-022332). |
| `SV-H02` | cumplida | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_spec2viz_notation_validates_the_same_as_the_sldb_builtin (8 casos: activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence; cada notación copiada de spec2viz `b624b75` carga con sldb, está en `builtin_notations()` y su `model_dump()` es igual al de la builtin de sldb) y test_builtin_notations_still_validate_and_are_unstyled. | - |
| `SV-H03` | cumplida | IR `tests/visual/test_notations_parity.py` (IR13g: 88 passed, 1 xfailed, el de SV-H01): las 10 no CLI de `tests/test_notation_view.py`, las 2 de `tests/test_view_contract_resolved.py` y test_resolve_documents_is_public_and_filters_relations (19 casos, sin xfail), contra `resolve_view`/`resolve_documents` de `sldb.api.notations`. G4 de graph_ui resuelto: master `79d63ee` (closeout `c9b09f7`, nota 20261116-131509) usa `sldb.api.notations` y no importa ni declara spec2viz. | - |
| `SV-H04` | cumplida | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_new_builtin_shapes_are_accepted, test_default_palette_is_accessible_and_distinguishable_without_colour, test_color_pair_is_validated_typed, test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not y test_palette_check_is_typed (6 casos: parte no CLI de test_palette_validation_is_typed, `check_palette(PaletteSpec.model_validate(raw))` de sldb con su error tipado y su mensaje), contra `sldb.notations` (vía `specir.visual.notation_style`). | - |
| `SV-H05` | cumplida | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin (la paleta `default` copiada de spec2viz `b624b75` carga y valida con `load_palette` de sldb y su `model_dump()` es igual al de la builtin `default` de sldb). | - |
| `SV-H06` | cumplida | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed): test_precedence_glyph_over_spec_over_palette, test_spec_style_kinds_are_validated_typed, test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec, test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched y test_mermaid_takes_the_light_side_of_a_spec_pair (las dos de mermaid contra `src/specir/visual/renderers/mermaid.py`, que usa la precedencia de sldb). | - |
| `SV-I01` | cumplida | sldb `tests/matching/test_matching_explicit.py` (10 passed); IR `tests/visual/test_catalog.py`, `tests/visual/test_catalog_parity.py` y `tests/test_imports.py` (9 passed). | - |
| `SV-I02` | cumplida | sldb `tests/matching/test_matching_fuzzy.py` (3 passed) y SV-G08 cumplida (IR `tests/visual/test_catalog.py`, 68 passed: test_label_key_of_sldb_is_the_template_s_norm_key y test_label_key_of_sldb_splits_underscores_like_norm_key sin xfail). | - |
| `SV-I03` | cumplida | sldb `tests/matching/test_matching_refs.py` (10 passed: los 9 de resolución y aristas de `tests/test_refs.py`); IR `tests/visual/test_refs_models.py` (12 passed: los 3 de modelos y schema, portados por IR13), `tests/visual/test_catalog_parity.py` (store de la vista) y `tests/test_imports.py`. | - |
| `SV-I04` | cumplida | sldb `tests/matching/test_matching_coverage.py` (3 passed); IR `tests/visual/test_catalog_parity.py` y `tests/visual/test_catalog.py`. | - |
| `SV-I05` | cumplida | IR `tests/visual/test_catalog_parity.py` (mismo resultado que `SldbAtomResolver` con `find_store` y `StoreReader` de sldb). | - |
| `SV-J01` | cumplida | IR `tests/visual/test_api.py` (test_load_*, test_validate_* contra `load_spec`/`validate_spec` de sldb). | - |
| `SV-J02` | cumplida | IR `tests/visual/test_api.py` (31 passed). | - |
| `SV-J03` | cumplida | IR `tests/visual/test_api.py`, `tests/visual/test_cli.py` y `tests/visual/test_render_commands.py`. | - |
| `SV-J04` | cumplida | IR `tests/visual/test_bpmn.py`, `tests/visual/test_resources.py` (test_examples_render_successfully) y `tests/visual/test_packaging.py` (3 passed). | - |
| `SV-J05` | cumplida | IR `tests/visual/test_resources.py` (la wheel lleva la plantilla) y `tests/visual/test_catalog.py` (la plantilla corrida con node). | - |
| `SV-J06` | cumplida | IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed) (SV-H02 y SV-H05 cumplidas: las notaciones y la paleta son las builtin de sldb); specIR no empaqueta notaciones ni paletas. | - |
| `SV-J07` | cumplida | IR `tests/visual/test_packaging.py` (venv limpio sin spec2viz). | - |
| `SV-J08` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-J09` | cumplida | IR `tests/visual/test_cli.py` (test_the_skill_names_only_commands_that_exist, test_the_skill_names_no_spec2viz_command). | - |
| `SV-K01` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-K02` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-K03` | cumplida | IR `tests/visual/test_cli.py`; SV-K04 a SV-K08 cumplidas. | - |
| `SV-K04` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-K05` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-K06` | cumplida | IR `tests/visual/test_cli.py` y `tests/visual/test_catalog_annotations.py`. | - |
| `SV-K07` | cumplida | IR `tests/visual/test_cli.py`; sldb `tests/notations/test_spec_catalog_sync.py`. | - |
| `SV-K08` | cumplida | IR `tests/visual/test_cli.py`; sldb `tests/notations/test_spec_catalog_sync.py`. | - |
| `SV-K09` | abierta | IR `tests/visual/test_cli.py`. | Depende de SV-K16 (SV-K12 ya cumplida). |
| `SV-K10` | cumplida | IR `tests/visual/test_cli.py`; sldb `tests/notations/test_notations_from_graph_cli.py` (6 passed). | - |
| `SV-K11` | cumplida | IR `tests/visual/test_cli.py`; sldb `tests/notations/test_component_spec_python.py`. | - |
| `SV-K12` | cumplida | IR `tests/visual/test_cli.py` (44 passed con `SPECIR_MMDC` apuntando a mermaid-cli real; test_lint_alias_matches_diagram_lint) y SV-D01 cumplida. | - |
| `SV-K13` | cumplida | IR `tests/visual/test_cli.py` y `tests/visual/test_render_commands.py`. | - |
| `SV-K14` | cumplida | IR `tests/visual/test_cli.py` y `tests/visual/test_schema.py`. | - |
| `SV-K15` | cumplida | IR `tests/visual/test_cli.py`; sldb `tests/notations/test_notations_sync_spec_cli.py` (4 passed) y `tests/notations/test_spec_sync.py`. | - |
| `SV-K16` | abierta | IR `tests/visual/test_cli.py` (test_validate_*, test_diagram_validate_*). | `specir diagram validate` es provisional: falta el comando de sldb que valide un spec (nota 20261115-192054) y retirar el de specIR. |
| `SV-K17` | cumplida | IR `tests/visual/test_cli.py` (44 passed con `SPECIR_MMDC` apuntando a mermaid-cli real; test_lint_alias_matches_diagram_lint, test_every_alias_stands_for_a_group_command_with_the_same_parameters) y SV-K12 cumplida. | - |
| `SV-K18` | abierta | IR `tests/visual/test_cli.py`. | Depende de SV-K21 (SV-K19, SV-K20 y SV-K22 ya cumplidas). |
| `SV-K19` | cumplida | IR `tests/visual/test_cli.py` y SV-H02 cumplida (IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed)). | - |
| `SV-K20` | cumplida | IR `tests/visual/test_cli.py` y SV-E02 cumplida (IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed)). | - |
| `SV-K21` | abierta | IR `tests/visual/test_cli.py` (invoca `load_notation`). | Depende de SV-H01; falta el comando de sldb que valide una notación (nota 20261115-192054). |
| `SV-K22` | cumplida | IR `tests/visual/test_cli.py` y SV-H03 cumplida (IR `tests/visual/test_notations_parity.py` (IR13g: 88 passed, 1 xfailed)). | - |
| `SV-K23` | abierta | IR `tests/visual/test_cli.py`. | Depende de SV-K26 (SV-K24 y SV-K25 ya cumplidas). |
| `SV-K24` | cumplida | IR `tests/visual/test_cli.py` y SV-H05 cumplida (IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed)). | - |
| `SV-K25` | cumplida | IR `tests/visual/test_cli.py` y SV-E02 cumplida (IR `tests/visual/test_notations_parity.py` (IR13e: 88 passed, 1 xfailed)). | - |
| `SV-K26` | abierta | IR `tests/visual/test_cli.py` (invoca `load_palette`). | Depende de SV-H04; falta el comando de sldb que valide una paleta (nota 20261115-192054). |
| `SV-K27` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-K28` | cumplida | IR `tests/visual/test_cli.py`. | - |
| `SV-K29` | abierta | IR `tests/visual/test_cli.py`. | Igual que SV-K16. |
| `SV-K30` | cumplida | IR `tests/visual/test_cli.py`. | - |

## Gate de retiro

Lista comprobable. spec2viz solo se retira cuando **todos** los ítems se cumplen; el procedimiento está en
`docs/spec2viz/gate-de-retiro.md` y lo evalúa IR13.

- [ ] **G1. Filas cumplidas.** Toda fila SV-* de esta matriz tiene su condición de retiro cumplida y la
  prueba que lo acredita citada por IR13 en la fila (ninguna fila sin prueba; ninguna dice descartado ni
  fuera de alcance).
  Estado IR13: **abierto**. 9 filas abiertas (sección «Acreditación (IR13)»; la corrida con mmdc del 2026-11-15 acreditó 7, IR13e, el 2026-11-16, otras 12, SV-G08 y SV-I02 incluidas, e IR13g, el mismo día, SV-H03 y SV-K22).
- [ ] **G2. Suite de spec2viz.** Cada caso de cada archivo de `spec2viz/tests/` pasa contra specIR o
  contra sldb (portado), o pertenece a una fila en modo reemplazar cuya prueba equivalente está declarada y
  pasa. La tabla «Pruebas de spec2viz por fila» no deja archivo sin fila.
  Estado IR13: **abierto**. IR13e portó contra sldb 42 pruebas de `tests/test_notation.py`, `tests/test_notation_view.py`, `tests/test_view_contract_resolved.py`, `tests/test_style_palette.py` y `tests/test_view_doc.py` (`tests/visual/test_notations_parity.py`; la parte de CLI de las 6 que invocan el CLI tiene su equivalente en las filas K, y la validación tipada sin CLI de dos de ellas está portada), con un xfail estricto en test_invalid_notations_are_rejected (SV-H01, nota a sldb 20261116-022332); los casos de mmdc ya corren con mermaid-cli real (0 skipped); el caso de `label_key` ya no es xfail (sldb `06dbcf02`, IR `4dc8946`). La tabla no deja archivo sin fila (`tests/test_matriz_cobertura_spec2viz.py`).
- [ ] **G3. CLI.** Cada comando y subgrupo de la ayuda de spec2viz (filas SV-K*) tiene equivalente que
  existe y una prueba lo invoca (`docs/spec2viz/correspondencia-cli.md` de IR13d).
  Estado IR13: **abierto**. Los 30 equivalentes existen y `test_every_equivalent_of_the_table_answers_its_help` los invoca, pero SV-K21 y SV-K26 no tienen comando en sldb y SV-K16/SV-K29 son provisionales en specIR.
- [ ] **G4. Consumidores.** Ningún consumidor del inventario importa ni invoca spec2viz: cero
  `import spec2viz`/`from spec2viz`, cero dependencias declaradas (pyproject, requirements, CI), cero
  invocaciones del comando `spec2viz` en código, scripts o configuración ejecutable, y ninguna habilidad de
  agente que instruya a invocarlo. El comprobador de IR13 sale con código distinto de cero si encuentra una.
  Estado IR13: **abierto**. `specir retirement check` (corrida del 2026-11-16 de IR13h, acta) lista 63 dependencias: sldb 1, las pruebas de paridad de IR 43 y el store `spec2viz/.sldb` 19 (G5); graph_ui, deskops y pron salen con 0.
- [ ] **G5. Stores.** Ningún store del universo registra modelos `spec2viz.sldb_models` en su
  `store.yaml`, su `store_index.yaml` ni sus `core/models/*.yaml`.
  Estado IR13: **abierto**. `spec2viz/.sldb` registra los 7 modelos de `spec2viz.sldb_models` (19 registros).
- [x] **G6. specIR limpio.** Ningún módulo bajo `src/specir/` importa spec2viz (prueba de imports) y specIR
  no define envoltorios de lo que se usa de sldb directamente.
  Estado IR13: **cumplido**. `tests/test_imports.py` (9 passed); specIR no define comandos de lo que es de sldb (`test_specir_defines_no_command_the_table_gives_to_sldb`).
- [x] **G7. Decisión del YAML.** La decisión sobre el YAML de spec frente al grafo
  (`docs/decisiones/fuente-de-verdad-del-diagrama.md`) está aceptada por JP y las filas marcadas con †
  están alineadas con ella.
  Estado: **cumplido**. JP aceptó la decisión el 2026-11-15 (vía supervisor): el YAML del spec queda como
  formato de autoría e intercambio subordinado al grafo (`docs/decisiones/fuente-de-verdad-del-diagrama.md`,
  atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`).
  Las filas con † quedan alineadas: la regla de rutas de deskops y los specs existentes (inventario de
  consumidores).
