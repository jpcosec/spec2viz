# Resultado del ejecutor deskops-e-3db2821b1604-a2 (IR13e, intento 2: ciclo de corrección 1)

Tarea: `task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`.
No hice commit, `git add` ni stash. No toqué `desk/` ni `.sldb/` a mano y no corrí la suite completa (la corre el tester bajo el lock).
Conservé y completé el trabajo del intento 1 (`runs/subagents/deskops-e-31500ac1cfa1/`); no rehíce nada.

## Revisiones

- spec2viz: `git -C ../spec2viz rev-parse --short HEAD` da **`91ba1d0`**, no `b624b75`. Es `b624b75` más un único commit de desk/store, y `git diff --stat b624b75 HEAD -- spec2viz/notations spec2viz/palettes tests` sale vacío (validation.log §1). Las pruebas de origen se leyeron con `git show b624b75:tests/test_style_palette.py`.
- sldb `3c2186de`; IR `8940470` más los cambios sin commitear de esta tarea; graph_ui `b868673`, con 48 rutas sin commitear en su árbol, que no son mías.

## Qué cambió respecto al intento 1

1. **`tests/visual/test_notations_parity.py`**:
   - Agregué `test_notation_load_gives_typed_errors` (e1), con los 7 casos de `test_notation_validate_gives_typed_errors` y `pytest.raises(error)` sobre `load_notation(path)`, sin CliRunner.
   - Agregué `test_palette_check_is_typed` (e2), con los 6 casos de `test_palette_validation_is_typed` y `pytest.raises(error, match=message)` sobre `check_palette(PaletteSpec.model_validate(raw))`. La paleta de partida es la copia `fixtures/spec2viz-notations/palettes/default.yml`; tampoco usa CliRunner.
   - Los docstrings citan la prueba de origen y dicen «parte no CLI».
   - Agregué los imports `PaletteSpec`, `UnknownKindError`, `UnknownShapeError` y `check_palette` desde `specir.visual.notation_style`, y actualicé el docstring del módulo con los totales 42 + 9 = 51.
   - Los 13 casos nuevos pasan contra sldb sin xfail, así que no hizo falta ninguna nota nueva a sldb.
2. **`src/specir/visual/notation_style.py`**: sin cambios en este intento. Ya reexportaba todo lo necesario desde el intento 1.
3. **`docs/spec2viz/matriz-de-cobertura.md`**:
   - SV-H01 suma test_notation_load_gives_typed_errors, pero sigue abierta por el xfail previo.
   - SV-H04 suma test_palette_check_is_typed y sigue cumplida.
   - SV-G08 y SV-I02 pasan a cumplidas.
   - SV-G03 deja de citar «1 xfailed de SV-G08».
   - La fila SV-G08 de la tabla principal ya no dice que el xfail sigue.
   - Recuentos 75→88 passed. Resumen 92/13 → **94/11**. Actualicé el párrafo IR13e y los estados de G1 y G2.
4. **`docs/spec2viz/acta-de-retiro.md`**: nueva salida del comprobador (85 dependencias, 11 filas), G1, G2, G4, filas de graph_ui y sldb en «Consumidores», «Lo que falta» punto 4 y el bloque de dependencias sustituido por la salida nueva.
5. **SV-H06** (revisada contra el contrato): se mantiene **cumplida**.
   - Su condición son «los casos de precedencia de test_style_palette.py», y el contrato, en la precisión (b), le asigna exactamente las 5 pruebas que cita. Las 5 pasan.
   - La objeción del tester del intento 1 (`deskops-t-5a39cc2dfbf8`) era que faltaba portar la validación tipada no CLI. La precisión (g) asigna esa validación a SV-H01 y SV-H04, no a SV-H06, y ya está portada.

## Las 51 pruebas (pytest: 88 passed, 1 xfailed, 89 casos con parametrize, 0 skipped)

Son 44 funciones `def test_`: 42 portadas y las 2 funciones de comparación, que con parametrize dan las 9 comparaciones. Todas pasan salvo el caso xfail indicado abajo.

- **Comparaciones «valida igual» (9):**
  - test_spec2viz_notation_validates_the_same_as_the_sldb_builtin, 8 casos;
  - test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin.
- **test_view_doc.py (3):** test_defaults_and_shape, test_invalid (4 casos) y test_view_doc_in_a_store_references_its_notation.
- **test_notation.py (12):**
  - test_builtins_load_and_cover_every_diagram_type
  - test_wildcard_link_and_free_relations
  - test_uml_class_notation_matches_the_class_spec_vocabulary
  - test_statechart_nests_contains_and_marks_the_initial_state
  - test_minimal_notation_defaults
  - test_invalid_notations_are_rejected (15 casos; **1 xfailed**, ver abajo)
  - test_free_relation_diagram_types_accept_any_relation
  - test_load_notation_from_path_and_unknown_name
  - test_notation_sync_writes_docs_and_edges
  - test_notation_sync_is_idempotent_and_prunes
  - test_notation_naming_an_unregistered_model_is_reported
  - test_wildcard_link_leaves_no_dangling_relation_type
- **test_notation_view.py (10):**
  - test_pure_helpers
  - test_class_view_picks_glyphs_by_where_and_links_by_relation
  - test_state_view_nests_contains_and_marks_initial
  - test_repo_pilot_with_a_composite_state_resolves_nest_and_a_crossing_transition
  - test_fragments_group_consecutive_messages
  - test_repo_sequence_pilot_has_loop_and_alt_fragments
  - test_view_errors
  - test_every_catalog_spec_resolves_under_its_builtin_notation
  - test_component_wildcard_link_and_sequence_order
  - test_activity_and_matrix_views
- **test_view_contract_resolved.py (2):** test_no_placeholder_reaches_the_render_contract (7 casos) y test_deployment_keyword_interpolates_kind_and_drops_when_empty.
- **test_style_palette.py (15):**
  - test_new_builtin_shapes_are_accepted
  - **test_notation_load_gives_typed_errors (7, nueva)**
  - test_builtin_notations_still_validate_and_are_unstyled
  - test_default_palette_is_accessible_and_distinguishable_without_colour
  - **test_palette_check_is_typed (6, nueva)**
  - test_precedence_glyph_over_spec_over_palette
  - test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched
  - test_spec_style_kinds_are_validated_typed (2)
  - test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend
  - test_unstyled_notation_writes_no_palette_and_no_style
  - test_resolve_documents_is_public_and_filters_relations
  - test_color_pair_is_validated_typed (4)
  - test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not
  - test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec
  - test_mermaid_takes_the_light_side_of_a_spec_pair

**El único xfail:** el xfail estricto viene del intento 1 y no cambió: `test_invalid_notations_are_rejected[changes1-not a spec2viz diagram type]`. sldb dice «diagram_type 'mindmap' is not a valid diagram type», donde spec2viz decía «not a spec2viz diagram type». Nota a sldb 20261116-022332.

## Las 18 filas (16 del scope más SV-G08 y SV-I02)

| Fila | Estado | Acredita / motivo | Cambio |
|---|---|---|---|
| SV-A17 | abierta | Sus 3 pruebas pasan con `ViewDoc` de `sldb.api`; falta solo G5 (nota a spec2viz 20261115-225013). | = |
| SV-E02 | cumplida | 4 de sync de test_notation.py y 2 de test_style_palette.py. | = |
| SV-H01 | abierta | Suma test_notation_load_gives_typed_errors (7 passed). Sigue abierta por el xfail estricto de test_invalid_notations_are_rejected[changes1] (nota 20261116-022332). | suma prueba |
| SV-H02 | cumplida | 8 comparaciones y test_builtin_notations_still_validate_and_are_unstyled. | = |
| SV-H03 | abierta | Sus 13 pruebas pasan; falta solo G4 de graph_ui (ver «Pendiente»). | = |
| SV-H04 | cumplida | Sus 4 pruebas anteriores más test_palette_check_is_typed (6 passed). | suma prueba |
| SV-H05 | cumplida | Comparación de la paleta default. | = |
| SV-H06 | cumplida | Las 5 pruebas de la precisión (b); revisada, ver arriba. | revisada |
| SV-J06 | cumplida | SV-H02 y SV-H05 cumplidas. | = |
| SV-K18 | abierta | Depende de SV-K21 (fuera de alcance) y SV-K22. | = |
| SV-K19 | cumplida | `tests/visual/test_cli.py` y SV-H02. | = |
| SV-K20 | cumplida | `tests/visual/test_cli.py` y SV-E02. | = |
| SV-K22 | abierta | Depende de SV-H03. | = |
| SV-K23 | abierta | Depende de SV-K26 (fuera de alcance). | = |
| SV-K24 | cumplida | `tests/visual/test_cli.py` y SV-H05. | = |
| SV-K25 | cumplida | `tests/visual/test_cli.py` y SV-E02. | = |
| SV-G08 | **cumplida** | `tests/visual/test_catalog.py` con `SPECIR_MMDC`: 68 passed, sin xfailed ni xpassed (`-rxX`). Pasan test_label_key_of_sldb_is_the_template_s_norm_key y test_label_key_of_sldb_splits_underscores_like_norm_key. | **nueva** |
| SV-I02 | **cumplida** | sldb `tests/matching/test_matching_fuzzy.py` (3 passed) y SV-G08 cumplida. | **nueva** |

En total, 12 cumplidas y 6 abiertas.

## Notas enviadas a sldb

- No envié ninguna nueva en este intento.
- Sigue vigente la del intento 1: `20261116-022332-suggestion-ir13e-mensaje-de-notationspec-ante-un-diagram-type-desconocido-difiere-del-de-spec2viz`, que cita el caso xfail de test_invalid_notations_are_rejected.

## specir retirement check

- **Resultado:** rc 1, que es lo esperado porque el gate sigue abierto.
- **Antes de IR13e:** 23 filas no acreditadas y 119 dependencias.
- **Después del intento 1:** 13 filas.
- **Ahora:** **11 filas** no acreditadas (SV-A17, H01, H03, K09, K16, K18, K21, K22, K23, K26 y K29) y **85 dependencias**.
- Las 11 son exactamente las abiertas de la matriz (94 cumplidas, 11 abiertas). Ninguna fila cumplida aparece como no acreditada.

Las dependencias bajan de 119 a 85 por cambios ajenos a esta tarea, y así lo anoté en el acta:

- **graph_ui:** pasa de 34 a 0, pero solo en su árbol de trabajo, que tiene 48 rutas sin commitear. Su HEAD `b868673` sigue con `from spec2viz.notation_view import …` (`sldb_adapter.py:245`, `:437`) y con `spec2viz>=0.1.0` en `pyproject.toml`. Por eso no lo di por resuelto: G4 de graph_ui sigue «pendiente (sin commit)» y SV-H03 sigue abierta.
- **sldb:** el oráculo de D2 se congeló en un golden en `ce0bd384`. La dependencia restante es ahora `runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5`.

## Validación (validation.log, cada comando con su rc)

| Comando | Resultado |
|---|---|
| `tests/visual/test_notations_parity.py` | 88 passed, 1 xfailed, rc 0 |
| `tests/test_imports.py` | 9 passed, rc 0 |
| `tests/test_matriz_cobertura_spec2viz.py` | 5 passed, rc 0 |
| `tests/visual/test_retirement_gate.py` | 6 passed, 1 xfailed (el xfail estricto del universo real, previo), rc 0 |
| `tests/visual/test_catalog.py` (`-rxX`, `SPECIR_MMDC` real) | 68 passed, sin xfailed ni xpassed, rc 0 |
| sldb `tests/matching/test_matching_fuzzy.py` | 3 passed, rc 0 |
| greps de imports prohibidos | sin coincidencias (rc 1 de grep en los dos) |
| `specir retirement check` | rc 1: 85 dependencias, 11 filas |
| `deskops graph missing --root .` | rc 0 |

No toqué `notation_style.py` en este intento. Aun así, sus importadores (`tests/test_imports.py`, `tests/visual/test_catalog.py` y `tests/visual/test_notations_parity.py`) quedaron corridos arriba.

Evidencia del estado del árbol: `git-status.txt` y `diff-stat.txt`.

- Fuera de `desk/`, `.sldb/` y `runs/` solo aparecen los 5 archivos de esta tarea, más `__pycache__` y egg-info.
- Los cambios de `.sldb/core/models/*.yaml`, `store_index.yaml` y la review bundle-3 de la tarea de MCP no son míos.

## Pendiente / bloqueado

- La suite completa bajo `flock /dev/shm/sldb1-tests.lock` la corre el tester.
- SV-H01 espera la respuesta de sldb a la nota 20261116-022332.
- SV-H03 y SV-K22 esperan a que graph_ui commitee su migración y responda con el commit. Hoy solo está en su árbol de trabajo.
- Quedan fuera de alcance:
  - SV-A17 (G5);
  - SV-K18, SV-K23, SV-K21 y SV-K26, que esperan los comandos de sldb (nota 20261115-192054).
- La revisión de spec2viz es `91ba1d0` en vez de `b624b75`; no afecta a los archivos usados.
