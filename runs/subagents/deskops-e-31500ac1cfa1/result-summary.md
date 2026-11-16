# Resultado del ejecutor deskops-e-31500ac1cfa1 (IR13e, intento 1)

Tarea: `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`
(contract_sha256 `5efb8cf1…2b59`). Sin commit, sin `git add`, sin tocar `desk/` ni `.sldb/` a mano, sin
suite completa (la corre el tester).

## Revisiones

- spec2viz: `git -C ../spec2viz rev-parse --short HEAD` da **`91ba1d0`**, no `b624b75`. `91ba1d0` es
  `b624b75` más un único commit de desk/store («desk: G5, decisión de JP (opción A)…»):
  `git diff --stat b624b75 HEAD -- spec2viz/notations spec2viz/palettes tests` sale vacío. Las copias se
  hicieron con `git show b624b75:<ruta>` (exactamente la revisión del contrato) y son idénticas a HEAD.
- sldb: `9307d485` (editable desde `../sldb/src`). IR: `37f41ee` + cambios sin commitear.

## Archivos tocados (solo los 5 del contrato)

- `tests/visual/test_notations_parity.py` (nuevo).
- `tests/visual/fixtures/spec2viz-notations/` (nuevo): `notations/{activity,component,component-view-matrix,deployment,reflection,statechart,uml-class,uml-sequence}.yml`, `palettes/default.yml`, `README.md` (una línea: revisión b624b75 y rutas de origen).
- `src/specir/visual/notation_style.py`: solo reexportaciones de `sldb.notations` (`SHAPES`, `DiagramType`, `InvalidColorError`, `NotationSpec`, `PaletteSpec`, `UnknownIconError`, `UnknownKindError`, `UnknownShapeError`, `ValidationError`, `check_palette`, `contrast`, `load_notation`, `resolve_color`), docstring y `__all__`. Nada definido.
- `docs/spec2viz/matriz-de-cobertura.md`: 16 filas de «Acreditación (IR13)», párrafo IR13e, resumen (92/13) y estados G1/G2 del gate.
- `docs/spec2viz/acta-de-retiro.md`: nueva salida del comprobador (resumen, G1, G2, G4, bloque de dependencias, «Lo que falta» punto 3).

Fuera de esos archivos, la única escritura fue la nota a sldb (abajo). Los cambios en `.sldb/` y `desk/` que
muestra `git-status.txt` ya estaban antes de empezar (Board, IR13, reviews de IR13e), no son míos.

Las pruebas no importan spec2viz ni `sldb.(notations|models|store|core)`: de sldb solo `sldb.api` y
`sldb.api.notations` (incluido `ViewDoc`, que sldb.api sí exporta); lo demás vía `specir.visual.notation_style`;
renderers de `specir.visual.renderers` (mermaid: `src/specir/visual/renderers/mermaid.py`). Fixtures de specs:
las copias ya existentes de spec2viz en `tests/visual/fixtures/spec2viz/` (idénticas a b624b75, verificado con
`cmp`) y el catálogo en `tests/visual/fixtures/catalog/docs/architecture/vistas.yml` (idéntico a b624b75).

## Las 49 pruebas (75 passed, 1 xfailed; 76 casos con parametrize, ninguno skipped)

Comparaciones «valida igual» (9):
- test_spec2viz_notation_validates_the_same_as_the_sldb_builtin × 8 (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence): passed.
- test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin: passed.

test_view_doc.py (3): test_defaults_and_shape, test_invalid (4 casos), test_view_doc_in_a_store_references_its_notation — passed.

test_notation.py (12 de 14; no CLI): test_builtins_load_and_cover_every_diagram_type, test_wildcard_link_and_free_relations, test_uml_class_notation_matches_the_class_spec_vocabulary, test_statechart_nests_contains_and_marks_the_initial_state, test_minimal_notation_defaults, test_free_relation_diagram_types_accept_any_relation, test_load_notation_from_path_and_unknown_name, test_notation_sync_writes_docs_and_edges, test_notation_sync_is_idempotent_and_prunes, test_notation_naming_an_unregistered_model_is_reported, test_wildcard_link_leaves_no_dangling_relation_type — passed. **test_invalid_notations_are_rejected**: 14 casos passed, 1 **xfailed** estricto: `[changes1-not a spec2viz diagram type]` — sldb rechaza `diagram_type: mindmap` con «diagram_type 'mindmap' is not a valid diagram type» (`sldb/src/sldb/notations/notation_spec.py:47`) donde spec2viz decía «not a spec2viz diagram type».

test_notation_view.py (10 de 11; no CLI): test_pure_helpers, test_class_view_picks_glyphs_by_where_and_links_by_relation, test_state_view_nests_contains_and_marks_initial, test_repo_pilot_with_a_composite_state_resolves_nest_and_a_crossing_transition, test_fragments_group_consecutive_messages, test_repo_sequence_pilot_has_loop_and_alt_fragments, test_view_errors, test_every_catalog_spec_resolves_under_its_builtin_notation, test_component_wildcard_link_and_sequence_order, test_activity_and_matrix_views — passed. (En test_class_view… spec2viz bifurcaba por `relation_doc_has_attributes()`; sldb actual guarda los atributos, se aserta esa rama, anotado en el docstring.)

test_view_contract_resolved.py (2): test_no_placeholder_reaches_the_render_contract (7 specs), test_deployment_keyword_interpolates_kind_and_drops_when_empty — passed.

test_style_palette.py (13 de 16; no CLI): test_new_builtin_shapes_are_accepted, test_builtin_notations_still_validate_and_are_unstyled, test_default_palette_is_accessible_and_distinguishable_without_colour, test_precedence_glyph_over_spec_over_palette, test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched, test_spec_style_kinds_are_validated_typed (2), test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend, test_unstyled_notation_writes_no_palette_and_no_style, test_resolve_documents_is_public_and_filters_relations, test_color_pair_is_validated_typed (4), test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not, test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec, test_mermaid_takes_the_light_side_of_a_spec_pair — passed.

No portadas (CLI, equivalentes en filas K / `tests/visual/test_cli.py`): test_cli_list_and_validate, test_cli_notation_sync, test_cli_view, test_notation_validate_gives_typed_errors, test_palette_validation_is_typed, test_palette_cli_sync_writes_the_store_document.

## Las 16 filas

| Fila | Estado | Acredita / motivo |
|---|---|---|
| SV-A17 | abierta | Las 3 de test_view_doc.py pasan con `ViewDoc` de `sldb.api`. Falta solo G5 (`spec2viz/.sldb` registra `spec2viz.sldb_models`; nota a spec2viz 20261115-225013; fuera de alcance). |
| SV-E02 | **cumplida** | 4 de sync de test_notation.py + 2 de sync de test_style_palette.py (y sldb `tests/notations/test_spec_sync.py`). |
| SV-H01 | abierta | xfail estricto de test_invalid_notations_are_rejected[changes1] (mensaje distinto); nota a sldb 20261116-022332. |
| SV-H02 | **cumplida** | 8 comparaciones + test_builtin_notations_still_validate_and_are_unstyled. |
| SV-H03 | abierta | Sus 13 pruebas pasan; falta solo G4 (graph_ui aún importa `spec2viz.notation_view`, `sldb_adapter.py:245`, `:437`, `tests/test_mindmap_notation.py:21`; pedido 20261115-224814). La condición de retiro de la fila incluye G4. |
| SV-H04 | **cumplida** | test_new_builtin_shapes_are_accepted, test_default_palette_is_accessible…, test_color_pair_is_validated_typed, test_single_hex… |
| SV-H05 | **cumplida** | Comparación de la paleta default. |
| SV-H06 | **cumplida** | test_precedence…, test_spec_style_kinds…, test_pair_reaches_the_view…, las 2 de mermaid. |
| SV-J06 | **cumplida** | SV-H02 y SV-H05 cumplidas; specIR no empaqueta notaciones ni paletas. |
| SV-K18 | abierta | Depende de SV-K21 (fuera de alcance) y SV-K22 (abierta). |
| SV-K19 | **cumplida** | `tests/visual/test_cli.py` + SV-H02. |
| SV-K20 | **cumplida** | `tests/visual/test_cli.py` + SV-E02. |
| SV-K22 | abierta | Depende de SV-H03 (solo G4). |
| SV-K23 | abierta | Depende de SV-K26 (fuera de alcance). |
| SV-K24 | **cumplida** | `tests/visual/test_cli.py` + SV-H05. |
| SV-K25 | **cumplida** | `tests/visual/test_cli.py` + SV-E02. |

10 pasan a cumplidas; 6 siguen abiertas.

## Notas enviadas a sldb

- `20261116-022332-suggestion-ir13e-mensaje-de-notationspec-ante-un-diagram-type-desconocido-difiere-del-de-spec2viz` (en `sldb/desk/inbox/`): cita `tests/visual/test_notations_parity.py::test_invalid_notations_are_rejected[changes1-not a spec2viz diagram type]` y `notation_spec.py:47`; pide decidir si conserva el mensaje de spec2viz o lo declara contrato.

## specir retirement check

rc 1 (esperado: gate abierto). Antes: 23 filas no acreditadas, 119 dependencias. Después: **13** filas no
acreditadas (SV-A17, G08, H01, H03, I02, K09, K16, K18, K21, K22, K23, K26, K29), 119 dependencias. Las 13
son exactamente las abiertas de la matriz (92 cumplidas / 13 abiertas); ninguna cumplida aparece como no
acreditada. (Las 122 dependencias del acta anterior ya eran 119 antes de IR13e: desaparecieron las 3 de
pron `docs/spec2viz/build.py:22-24`, cambio ajeno; anotado en el acta.)

## Validación (detalle en validation.log)

- test_notations_parity.py: 75 passed, 1 xfailed, rc 0.
- test_imports.py: 9 passed, rc 0. test_matriz_cobertura_spec2viz.py: 5 passed, rc 0. test_retirement_gate.py: 6 passed, 1 xfailed (el xfail estricto previo del universo real), rc 0.
- greps de imports prohibidos: sin coincidencias (rc 1 de grep = nada encontrado).
- `deskops graph missing --root .`: rc 0.
- Por tocar notation_style.py: tests/visual/test_catalog.py (con SPECIR_MMDC) 67 passed, 1 xfailed (SV-G08 previo), rc 0. tests/test_imports.py ya arriba.

## Pendiente / bloqueado

- Suite completa bajo `flock /dev/shm/sldb1-tests.lock`: no corrida (la corre el tester, según el brief).
- SV-H01: espera respuesta de sldb a la nota 20261116-022332.
- SV-A17 (G5), SV-H03/SV-K22 (G4 graph_ui), SV-K18/SV-K23 (SV-K21/K26, comando de sldb): fuera de alcance.
- Discrepancia de revisión de spec2viz (91ba1d0 vs b624b75) anotada arriba; sin efecto en los archivos usados.
- `src/specir.egg-info/` y `__pycache__/` sin trackear ya existían (instalación editable), no los creé para la tarea.
