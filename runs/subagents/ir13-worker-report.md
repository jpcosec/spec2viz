# Informe del worker IR13

Tarea: `task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`. Trabajé directo en IR main,
sin push. En esta corrida se evaluó el gate y se acreditó la matriz. **No se retiró spec2viz.** No toqué
código, dependencias ni stores de otros repos; solo dejé mensajes en sus inbox.

**Resultado: gate no cumplido; retiro no declarado. La tarea sigue abierta.** El estado quedó en el
Implementation Path, vía `deskops edit task`.

## Commits

| sha | Qué |
|---|---|
| `1f9251d` | Código y documentos: `specir retirement check` (`src/specir/visual/retirement.py`, subcomando en `src/specir/cli.py`), `tests/visual/test_retirement_gate.py` y `tests/visual/test_refs_models.py`; matriz con la sección «Acreditación (IR13)» y el estado de G1 a G7; `docs/spec2viz/acta-de-retiro.md`; `gate-de-retiro.md` nombra el comprobador. |
| `76d7bd0` | desk: precisiones de preflight-3, estado del gate y `files` de la tarea (todo con `deskops edit task`); repos deskops, pron, graph-ui y spec2viz registrados con `deskops repo register`; review preflight-3 dispuesta como `accepted`. |
| `c70f050` | `format_report` pasa a llamarse `format_gate_report`. |
| (último) | desk: precisiones de bundle-2, review bundle-2 dispuesta e informe. |

## Gate G1 a G7

| Ítem | Estado | Evidencia |
|---|---|---|
| G1 Filas | **abierto** | 75 cumplidas y 30 abiertas (detalle más abajo). |
| G2 Suite de spec2viz | **abierto** | Faltan por portar `test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py`, `test_style_palette.py` y `test_view_doc.py`. Además, los casos de mmdc se saltan y el de `label_key` es un xfail estricto. Los 38 archivos tienen fila (`test_matriz_cobertura_spec2viz.py`, 5 passed). |
| G3 CLI | **abierto** | Los 30 equivalentes existen y `test_every_equivalent_of_the_table_answers_its_help` los invoca (44 passed). Faltan en sldb los comandos para validar notación y paleta (K21, K26); el de validar un spec (K16, K29) sigue provisional en specIR. |
| G4 Consumidores | **abierto** | `specir retirement check` encuentra 122 dependencias (ver abajo). |
| G5 Stores | **abierto** | `spec2viz/.sldb` registra los 7 modelos de `spec2viz.sldb_models`: 19 registros entre `store.yaml:44-56`, `core/store_index.yaml:141-259` y `core/models/*.yaml:2`. Es el único store del universo que lo hace. |
| G6 specIR limpio | **cumplido** | `tests/test_imports.py` (9 passed) y `test_specir_defines_no_command_the_table_gives_to_sldb`. |
| G7 Decisión del YAML | **abierto** | `docs/decisiones/fuente-de-verdad-del-diagrama.md` sigue como propuesta pendiente de JP. |

## Filas: 75 cumplidas y 30 abiertas

Por modo:

| Modo | Cumplidas | Abiertas |
|---|---|---|
| migrar tal cual (52) | 43 | 9: B03, C13, C14, D01 y G03 (mmdc); G08 (`label_key`); K09, K12 y K17 (por dependencia) |
| reemplazar (4) | 4 (G06, J07, J09, K06) | 0 |
| migrado a sldb (30) | 27 | 3: K16 y K29 (validate provisional), I02 (depende de G08) |
| usar sldb directamente (19) | 1 (I05) | 18: A17, E02, H01 a H06, J06, K18 a K26 |

Por qué quedan abiertas:

- **Pruebas no portadas.** Las filas «usar sldb directamente» de notaciones, paletas y ViewDoc no tienen sus pruebas portadas a sldb desde que se retiró IR13c. sldb sí tiene pruebas propias de esas funciones (`test_notation_models_and_builtins.py`, 15 passed; `test_notation_view_and_routes.py`, 9 passed), pero no son los casos de spec2viz.
- **SV-K16 y K29.** `specir diagram validate` es provisional; el comando de sldb sigue pedido (nota `20261115-192054`). De esa misma nota dependen K21 y K26.
- **mmdc.** No se pudo correr la suite con mermaid-cli. Instalé `@mermaid-js/mermaid-cli` en `/dev/shm/ir13-mmdc` y ya lo borré. El modo automático me **denegó lanzar `/usr/bin/google-chrome`** como navegador de puppeteer. Para cerrar esas filas hace falta **permiso para ejecutar mmdc con Chrome** (o instalar mmdc con su Chromium) y correr `tests/visual/test_lint_mermaid.py` y `tests/visual/test_render_cases.py`.
- **SV-G08 e I02.** Hay un xfail estricto de `label_key`; está pedido en `20261115-214942`.

Cumplidas con prueba nueva: SV-I03. Porté los 3 casos de modelos y schema de `test_refs.py` en `tests/visual/test_refs_models.py` (12 passed). Los 9 de resolución ya estaban portados en sldb `tests/matching/test_matching_refs.py`. Con eso queda resuelto el pendiente 4 de la matriz.

## Consumidores pendientes: archivo, línea y clase

Salida completa en `docs/spec2viz/acta-de-retiro.md`. Resumen:

- **graph_ui (34)**:
  - 9 importaciones: `frontends/mindmap/sldb_adapter.py:245` y `:437` (`from spec2viz.notation_view import …`); en pruebas, `test_projection_views.py:18,167`, `test_mindmap_notation.py:20,21`, `e2e_notation_legibility.py:38`, `e2e_mindmap_notation.py:27` y `e2e_review_workbench_views.py:40`.
  - 3 dependencias declaradas: `pyproject.toml:19`, `:24` y `.github/requirements-suite.txt:10`.
  - 22 invocaciones de `spec2viz diagram sync` y `shutil.which("spec2viz")`, todas en `tests/`.
- **deskops (22)**:
  - 20 de habilidad de agente: `.claude/skills/deskops-workflow/SKILL.md:27,59,60,101,102,103`, `references/spec2viz-cli.md:8-84` y `.opencode/skills/use-spec2viz/SKILL.md:2`.
  - 2 invocaciones: `desk/drawer/plans/workspace-documental/render_diagram.py:7` y `:9`.
  - No es dependencia: la regla `deskops/graph/desk_graph.py:75`, que espera a G7.
- **pron (3)**: invocaciones en `docs/spec2viz/build.py:22,23,24`.
- **sldb (1)**:
  - Una importación: `tests/notations/test_component_spec_python.py:43`, oráculo de D2 con `importorskip`.
  - Fuera del comprobador: `docs/architecture/spec2viz/vistas.yml`, que se construye con `spec2viz catalog build`, y `contracts/identity.toml:299`.
- **IR (43)**:
  - Importaciones de los oráculos de paridad en pruebas: `tests/visual/parity.py`, `render_parity.py`, los `importorskip` de las pruebas de paridad y `tests/test_matriz_cobertura_spec2viz.py:31`. Se saltan sin spec2viz.
  - Fuera del comprobador: `tests/conftest.py:24,80` y `test_mcp_extension.py:24` federan `spec2viz/.sldb`; la suite falla si ese store desaparece.
- **store `spec2viz/.sldb` (19)**: los modelos registrados de G5.

## Mensajes enviados (`deskops message send`)

Antes de enviar, registré deskops, pron, graph_ui (id `graph-ui`) y spec2viz en `desk/registry` de IR con `deskops repo register`, porque `--to` solo resolvía sldb. Las notas quedan sin commitear en cada repo destino.

| Destino | Nota |
|---|---|
| deskops | `deskops/desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md` |
| graph_ui | `UIs/graph_ui/desk/inbox/20261115-224814-suggestion-ir13-pide-migrar-graph-ui-de-spec2viz-a-sldb-resolve-view-sync-de-specs-viewdoc-pilotos.md` |
| pron | `pron/desk/inbox/20261115-224816-suggestion-ir13-pide-pasar-docs-spec2viz-build-py-de-pron-de-spec2viz-a-specir.md` |
| sldb (consumidor) | `sldb/desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md` |
| sldb (rendimiento) | `sldb/desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md` |
| spec2viz (store, G5) | `spec2viz/desk/inbox/20261115-225013-suggestion-ir13-el-store-de-spec2viz-es-el-nico-que-registra-spec2viz-sldb-models-gate-g5.md` |

## Medición de `specir catalog build` (pendiente de IR13d)

Con `examples/catalog/project.yml` dentro de IR, `timeout 300` lo corta: rc 124 a los 5 min, con 3 min 50 s de CPU. Volví a perfilar con cProfile (corte a los 150 s y volcado de pilas cada 60 s):

- 146 de 149 s se van en `sldb.api.matching.attach_atom_edges`: 31 llamadas a `StoreReader.edges_of` que generan 62 llamadas a `load_edge_index`, de ~1,1 s cada una.
- `with_live_stale` recalcula el stale vivo en cada llamada: 284 251 `_moved`, 63 s.
- Como hay stale, devuelve un `model_copy` nuevo cada vez, y `_ensure_maps` reconstruye los mapas cada vez (61 veces, 66 s).
- El store descubierto es el `.sldb` de IR. Federa 8 stores, con `deskops` y `sldb` duplicados desde `/mnt/ssd/herramientas`. `load_edge_index` tarda 28,6 s la primera vez y 0,4 s las siguientes, con un objeto distinto cada vez y 1963 stale.

**Es de sldb**: specIR solo usa la API pública. Lo pedí a su inbox con tres opciones de arreglo y la forma de reproducirlo. En specIR no hay nada que arreglar.

## Comprobador

- Subcomando: `specir retirement check [--matrix …] --path NOMBRE=RUTA …`.
- Cuándo falla:
  - rc 1 si encuentra alguna dependencia o alguna fila sin acreditar;
  - rc 2 si un nombre no está en el inventario o falta la ruta de uno que sí está.
- Qué detecta:
  - en Python, por AST: imports, `importorskip`/`import_module` y llamadas cuyo comando es `spec2viz`;
  - requisitos declarados en pyproject, setup, requirements y CI;
  - `spec2viz <subcomando>` en sh, Makefile y CI;
  - habilidades de agente que lo nombran como código o que se llaman como spec2viz;
  - `spec2viz.sldb_models` en los índices de store.
- Qué no cuenta: prosa, documentación, comentarios, docstrings, changelogs ni desk.
- Sobre el universo real: rc 1, 122 dependencias y 30 filas abiertas, en 3,6 s.

## Tests (TMPDIR=/dev/shm)

Cada archivo por separado, IR:

| Archivo | rc | Resultado |
|---|---|---|
| tests/test_imports.py | 0 | 9 passed |
| tests/test_matriz_cobertura_spec2viz.py | 0 | 5 passed (también después de editar la matriz) |
| tests/test_mcp_extension.py | 0 | 5 passed |
| tests/visual/test_api.py | 0 | 31 passed |
| tests/visual/test_bpmn.py | 0 | 26 passed |
| tests/visual/test_catalog.py | 0 | 67 passed, 1 xfailed |
| tests/visual/test_catalog_annotations.py | 0 | 5 passed |
| tests/visual/test_catalog_parity.py | 0 | 29 passed |
| tests/visual/test_cli.py | 0 | 44 passed |
| tests/visual/test_lint_mermaid.py | 0 | 8 passed, 7 skipped (mmdc) |
| tests/visual/test_packaging.py | 0 | 3 passed |
| tests/visual/test_render_cases.py | 0 | 27 passed, 3 skipped (mmdc) |
| tests/visual/test_render_commands.py | 0 | 33 passed |
| tests/visual/test_render_parity.py | 0 | 81 passed |
| tests/visual/test_renderers.py | 0 | 56 passed |
| tests/visual/test_resources.py | 0 | 7 passed |
| tests/visual/test_schema.py | 0 | 13 passed |
| tests/visual/test_sync_generation_parity.py | 0 | 22 passed |
| tests/visual/test_visual_compilers.py | 0 | 28 passed |
| tests/visual/test_visual_ir.py | 0 | 3 passed |
| tests/visual/test_visual_names.py | 0 | 4 passed |
| tests/visual/test_visual_normalize.py | 0 | 5 passed |
| tests/visual/test_visual_parity.py | 0 | 90 passed |
| tests/visual/test_visual_projections.py | 0 | 9 passed |
| tests/models/test_blog_chain.py | 0 | 7 passed, 2 xfailed |
| tests/models/test_domain_models.py | 0 | 7 passed |
| tests/models/test_domain_tools.py | 0 | 5 passed |
| tests/visual/test_retirement_gate.py (nuevo) | 0 | 6 passed, 1 xfailed (estricto: universo real) |
| tests/visual/test_refs_models.py (nuevo) | 0 | 12 passed |

Pruebas portadas de sldb, corridas con el entorno de IR (sldb editable desde `sldb/src`, porque `sldb/.venv` no tiene pytest), sin escribir caché: todas con rc 0.

| Archivo | Resultado |
|---|---|
| tests/notations/test_component_spec_graph.py | 16 passed |
| tests/notations/test_component_spec_python.py | 4 passed |
| tests/notations/test_notation_models_and_builtins.py | 15 passed |
| tests/notations/test_notation_view_and_routes.py | 9 passed |
| tests/notations/test_notations_from_graph_cli.py | 6 passed |
| tests/notations/test_notations_sync_spec_cli.py | 4 passed |
| tests/notations/test_spec_base_model.py | 3 passed |
| tests/notations/test_spec_catalog_sync.py | 8 passed |
| tests/notations/test_spec_class_diagram.py | 17 passed |
| tests/notations/test_spec_class_packages.py | 7 passed |
| tests/notations/test_spec_exceptions.py | 2 passed |
| tests/notations/test_spec_loader.py | 20 passed |
| tests/notations/test_spec_models_*.py (6 archivos) | 3, 3, 4, 4, 3 y 3 passed |
| tests/notations/test_spec_sync.py | 16 passed |
| tests/notations/test_spec_validator.py | 19 passed |
| tests/matching/test_matching_coverage.py | 3 passed |
| tests/matching/test_matching_explicit.py | 10 passed |
| tests/matching/test_matching_fuzzy.py | 3 passed |
| tests/matching/test_matching_refs.py | 10 passed |
| tests/test_linked_doc_refs.py | 20 passed |

Suite completa de IR con `-n 4`, sin tocar desk mientras corría: **rc 0, 647 passed, 10 skipped (mmdc), 4 xfailed**. Fue la segunda corrida. La primera dio rc 1: `test_imports.py::test_specir_defines_no_spec_sync_and_no_spec_generator` fallaba porque `retirement.py` definía `format_report`, un nombre que es de sldb. Lo renombré a `format_gate_report` (`c70f050`) y después pasaron `test_imports.py` (9), `test_retirement_gate.py` (6 y 1 xfailed) y `test_cli.py` (44).

## graph missing

`deskops graph missing --root .`: 0, con rc 0. Antes eran 3; desaparecieron los 3 de IR13: `acta-de-retiro.md` ×2 y `test_retirement_gate.py`.

## Revisión

- **preflight-3**: la corrí con `--force`, con el motivo de que la TaskDoc se reescribió el 2026-11-15, después de preflight-2. Resolví sus 5 ambigüedades en el Implementation Path y la dispuse como `accepted`.
- **bundle-2**: hecha después de la suite verde. Resolví sus 3 ambigüedades en el Implementation Path (Precisiones bundle-2) y la dispuse como `accepted`.

## Limpieza

Borré lo mío en `/dev/shm`: `ir13-*` (logs, textos, script de pruebas, perfiles, html, `ir13-bt/` con los basetemps, `ir13-mmdc/`). No toqué nada ajeno. No quedan procesos míos.

## Qué falta para poder retirar spec2viz

Lo que decide JP va aparte, al final.

1. **G4.** Que graph_ui, deskops, pron y sldb resuelvan los pedidos y respondan con el commit, que hay que registrar en el acta.
2. **G2 y G1.** Portar contra la API de sldb, sin envoltorio, los casos de:
   - `tests/test_notation.py`;
   - `tests/test_notation_view.py`;
   - `tests/test_view_contract_resolved.py`;
   - `tests/test_style_palette.py`;
   - `tests/test_view_doc.py`.

   Eso cierra SV-A17, E02, H01 a H06, J06 y K18 a K25 (K21 y K26 necesitan además el comando de sldb del punto 3). Hoy ninguna tarea lo tiene: conviene derivar una tarea en IR, o en sldb.
3. **sldb.** Lo que tiene que publicar sldb:
   - el comando para validar spec, notación y paleta, y después retirar `specir diagram validate`/`validate` (K16, K21, K26, K29);
   - el arreglo de `label_key` con `_` (G08, I02);
   - el arreglo de rendimiento de `matching`/edges.
4. **mmdc.** Correr con mermaid-cli las pruebas de B03, C13, C14, D01 y G03; de ellas dependen K09, K12 y K17. Hace falta **permiso para lanzar Chrome** desde mmdc, o una instalación de mmdc con su propio Chromium.
5. **IR.** Antes del retiro hay que:
   - quitar los oráculos de paridad que ya tienen goldens;
   - congelar como golden la paridad del catálogo de IR13b;
   - cambiar la federación de `spec2viz/.sldb` en `tests/conftest.py` por un fixture.

   Después, quitar el xfail de `test_the_real_universe_has_no_dependency_and_every_row_is_accredited`.
6. **G5.** Reapuntar o archivar el store `spec2viz/.sldb`, según decida el dueño de spec2viz.

**Lo decide JP:**
- G7, la decisión del YAML de spec frente al grafo;
- qué hacer con `desk_graph.py:75` de deskops y con los specs de `docs/architecture/spec2viz` de sldb una vez decidido G7;
- archivar o borrar spec2viz cuando el comprobador salga con rc 0.
