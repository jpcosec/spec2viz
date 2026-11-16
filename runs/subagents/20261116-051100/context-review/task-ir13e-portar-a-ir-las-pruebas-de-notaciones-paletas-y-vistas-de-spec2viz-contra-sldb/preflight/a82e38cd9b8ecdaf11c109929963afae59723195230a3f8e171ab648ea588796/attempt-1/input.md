FILE:desk/tasks/task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb.md
---
sldb:
  by: agent
  at: '2026-11-16T05:10:35Z'
  authority: generated
  via: save_document_payload
id: task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
- host:robocop2
current_node: ritual-execution
history: []
references:
- task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
- desk/reviews/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz/bundle-2.md
depends_on:
- task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- tests/visual/test_notations_parity.py
- tests/visual/fixtures/spec2viz-notations/
- src/specir/visual/notation_style.py
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/acta-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
---

# IR13e Portar a IR las pruebas de notaciones, paletas y vistas de spec2viz contra sldb

## Rationale

_Explain why this task exists or the business driver behind it._

IR13 (gate de retiro de spec2viz) tiene 23 filas abiertas en la sección «Acreditación (IR13)» de docs/spec2viz/matriz-de-cobertura.md. Varias filas en modo «usar sldb directamente» siguen abiertas solo porque sus casos de prueba de spec2viz no se han portado contra sldb: SV-A17, SV-E02, SV-H01 a SV-H06 y SV-J06, y de ellas dependen SV-K19, SV-K20, SV-K22, SV-K24 y SV-K25. La precisión 2 de bundle-2 de IR13 dice que portar esas pruebas es aportar evidencia (no implementar capacidades) y que le corresponde a IR13 o a una tarea derivada. Esta es esa tarea derivada: el único trabajo de IR13 que se puede hacer dentro de IR sin esperar a otros desks.

## Goal

_Describe the concrete result this task must produce._

Un archivo de pruebas de IR que ejecuta, contra sldb, 40 casos de las pruebas de spec2viz de notaciones, paletas y vistas, más 9 comparaciones «valida igual» (8 notaciones y la paleta default de spec2viz frente a las builtin de sldb), y la matriz de cobertura actualizada: cada fila listada queda cumplida citando esas pruebas o sigue abierta con la diferencia concreta y la nota enviada al desk de sldb.

## Scope

_State what is in scope and what is out of scope._

Dentro: (1) copiar como datos de prueba, sin importar spec2viz, las 8 notaciones de ../spec2viz/spec2viz/notations/*.yml y la paleta ../spec2viz/spec2viz/palettes/default.yml en la revisión b624b75 de spec2viz a tests/visual/fixtures/spec2viz-notations/, con un README.md de una línea que diga la revisión y la ruta de origen; (2) portar los casos de ../spec2viz/tests/test_view_doc.py (3 pruebas), test_notation.py (14), test_notation_view.py (11), test_view_contract_resolved.py (2) y test_style_palette.py (16) a tests/visual/test_notations_parity.py, ejecutándolos contra sldb y no contra spec2viz. Cada prueba portada lleva en su docstring el nombre de la prueba de spec2viz de la que sale. Las 6 pruebas de spec2viz que invocan su CLI (spec2viz.cli.main: test_cli_list_and_validate, test_cli_notation_sync, test_cli_view, test_notation_validate_gives_typed_errors, test_palette_validation_is_typed y test_palette_cli_sync_writes_the_store_document) no se portan aquí: su equivalente son las filas K, que ya citan tests/visual/test_cli.py de IR. Quedan 40 pruebas a portar. Las que usan un store (fixture store de test_notation.py) crean el suyo con sldb.api.init_store(tmp_path), como hace spec2viz, nunca sobre un store real; (3) las comparaciones «valida igual»: cada una de las 8 notaciones copiadas carga y valida con sldb y su contenido modelado es igual al de la builtin de sldb del mismo nombre, y la paleta default copiada es igual a la builtin default de sldb; (4) actualizar en la sección «Acreditación (IR13)» de docs/spec2viz/matriz-de-cobertura.md las filas SV-A17, SV-E02, SV-H01, SV-H02, SV-H03, SV-H04, SV-H05, SV-H06, SV-J06, SV-K18, SV-K19, SV-K20, SV-K22, SV-K23, SV-K24 y SV-K25, y el resumen de cumplidas/abiertas; (5) anotar en docs/spec2viz/acta-de-retiro.md la nueva salida de specir retirement check. Fuera: cambiar código de sldb o de spec2viz; implementar notaciones, paletas o vistas en specIR (son de sldb); las filas SV-G08, SV-I02, SV-K09, SV-K16, SV-K21, SV-K26 y SV-K29, que esperan cambios de sldb (notas 20261115-214942 y 20261115-192054); la parte G5 de SV-A17 (store spec2viz/.sldb, desk de spec2viz); cambiar modos o condiciones de retiro de IR07; declarar el retiro.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las pruebas importan de sldb solo sldb.api (sldb.api.notations exporta resolve_view, render_template, render_keyword, flatten, fragments_of, lookup, ViewError y la sincronización de notaciones y paletas). Lo que sldb.api todavía no exporta (load_notation, builtin_notations, DEFAULT_NOTATIONS, NotationSpec, load_palette, check_palette, contrast, PaletteSpec, resolve_style y los errores de sldb.notations) se toma de src/specir/visual/notation_style.py, el único módulo de specIR autorizado a importar sldb.notations (tests/test_imports.py): se agregan ahí como reexportaciones los nombres que falten, sin definir nada nuevo, y se actualiza su docstring y __all__. ViewDoc se toma de sldb.api si sldb lo exporta; si no, la fila SV-A17 queda abierta diciendo que falta exportarlo y se pide a sldb con deskops message send --to sldb. Cuando un caso portado no pasa contra sldb (otra clase de error, otro mensaje, otro resultado) o una comparación «valida igual» encuentra diferencias, no se ajusta la expectativa para que pase: el caso se marca pytest.mark.xfail(strict=True) con la diferencia en reason, la fila queda abierta con esa diferencia en «lo que falta», y se envía una nota al desk de sldb con deskops message send --to sldb --root . citando la prueba. Una fila pasa a cumplida solo si todas sus pruebas citadas pasan sin xfail; las filas K dependientes se acreditan citando tests/visual/test_cli.py cuando todas las filas de las que dependen quedan cumplidas, y si no, siguen abiertas. Archivos: tests/visual/test_notations_parity.py (nuevo), tests/visual/fixtures/spec2viz-notations/ (nuevo), src/specir/visual/notation_style.py, docs/spec2viz/matriz-de-cobertura.md, docs/spec2viz/acta-de-retiro.md. Comandos desde la raíz de IR con TMPDIR=/dev/shm y el .venv del repo. Precisiones (preflight-1): (a) Las comparaciones «valida igual» son 9 casos: uno por cada notación copiada (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence) frente a la builtin de sldb del mismo nombre, y uno para la paleta default; con pytest.mark.parametrize cuentan como 9 pruebas. (b) Correspondencia prueba→fila, que es la que se cita en «Acreditación (IR13)»: SV-A17 ← las 3 de test_view_doc.py; SV-H01 ← de test_notation.py, test_builtins_load_and_cover_every_diagram_type, test_wildcard_link_and_free_relations, test_uml_class_notation_matches_the_class_spec_vocabulary, test_statechart_nests_contains_and_marks_the_initial_state, test_minimal_notation_defaults, test_invalid_notations_are_rejected, test_free_relation_diagram_types_accept_any_relation y test_load_notation_from_path_and_unknown_name; SV-E02 ← test_notation_sync_writes_docs_and_edges, test_notation_sync_is_idempotent_and_prunes, test_notation_naming_an_unregistered_model_is_reported y test_wildcard_link_leaves_no_dangling_relation_type de test_notation.py, más test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend y test_unstyled_notation_writes_no_palette_and_no_style de test_style_palette.py; SV-H02 ← las 8 comparaciones de notaciones y test_builtin_notations_still_validate_and_are_unstyled; SV-H03 ← las 10 no CLI de test_notation_view.py, las 2 de test_view_contract_resolved.py y test_resolve_documents_is_public_and_filters_relations; SV-H04 ← test_new_builtin_shapes_are_accepted, test_default_palette_is_accessible_and_distinguishable_without_colour, test_color_pair_is_validated_typed y test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not; SV-H05 ← la comparación de la paleta default; SV-H06 ← test_precedence_glyph_over_spec_over_palette, test_spec_style_kinds_are_validated_typed, test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec, test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched y test_mermaid_takes_the_light_side_of_a_spec_pair (las dos de mermaid se portan contra el renderer de specIR, specir.visual, que usa la precedencia de sldb). Son 40 pruebas portadas. (c) Filas K dependientes, según la columna «lo que falta» de la matriz: SV-J06 ← SV-H02 y SV-H05; SV-K19 ← SV-H02; SV-K20 ← SV-E02; SV-K22 ← SV-H03; SV-K24 ← SV-H05; SV-K25 ← SV-E02; SV-K18 ← SV-K19, K20, K21 y K22; SV-K23 ← SV-K24, K25 y K26. SV-K21 y SV-K26 están fuera de alcance (esperan un comando de sldb), así que SV-K18 y SV-K23 siguen abiertas en esta tarea; solo se actualiza su texto de «lo que falta». (d) Si una prueba de una fila no puede pasar (por ejemplo, si sldb.api no exporta ViewDoc), solo esa fila queda abierta; el resto de las pruebas y filas se portan y acreditan igual.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_notations_parity.py sale con rc 0 y reporta las 40 pruebas portadas más las 9 comparaciones «valida igual» (passed o xfailed estricto, ninguna skipped).
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- grep -rnE '^(from|import) spec2viz' tests/visual/test_notations_parity.py no encuentra nada, y grep -rnE 'from sldb\.(notations|models|store|core)' tests/visual/test_notations_parity.py tampoco.
- timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb lista como no acreditadas solo filas que siguen abiertas en la matriz con su motivo, y ninguna de las filas que la matriz da por cumplidas; su salida queda en docs/spec2viz/acta-de-retiro.md.
- {'Suite completa una vez, bajo flock /dev/shm/sldb1-tests.lock': 'SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.'}
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

tests/visual/test_notations_parity.py existe y pasa (rc 0) contra sldb sin importar spec2viz; cada una de las 16 filas listadas en el scope está, en «Acreditación (IR13)», como cumplida citando una prueba que pasa, o como abierta con la diferencia concreta y la referencia de la nota enviada a sldb; el resumen de la matriz y el acta reflejan la nueva salida de specir retirement check; la suite completa pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

