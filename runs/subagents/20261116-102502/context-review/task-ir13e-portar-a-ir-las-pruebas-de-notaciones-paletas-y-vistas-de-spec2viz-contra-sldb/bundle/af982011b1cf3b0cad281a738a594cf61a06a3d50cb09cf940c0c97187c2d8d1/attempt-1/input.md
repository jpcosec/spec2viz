FILE:desk/tasks/task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb.md
---
sldb:
  by: agent
  at: '2026-11-16T10:24:12Z'
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
- task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents
- task-quitar-el-xfail-obsoleto-de-label-key-en-test-catalog-tras-el-arreglo-de-sldb-06dbcf02
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

Dentro: (1) copiar como datos de prueba, sin importar spec2viz, las 8 notaciones de ../spec2viz/spec2viz/notations/*.yml y la paleta ../spec2viz/spec2viz/palettes/default.yml en la revisión b624b75 de spec2viz a tests/visual/fixtures/spec2viz-notations/, con un README.md de una línea que diga la revisión y la ruta de origen; (2) portar los casos de ../spec2viz/tests/test_view_doc.py (3 pruebas), test_notation.py (14), test_notation_view.py (11), test_view_contract_resolved.py (2) y test_style_palette.py (16) a tests/visual/test_notations_parity.py, ejecutándolos contra sldb y no contra spec2viz. Cada prueba portada lleva en su docstring el nombre de la prueba de spec2viz de la que sale. Las 6 pruebas de spec2viz que invocan su CLI (spec2viz.cli.main: test_cli_list_and_validate, test_cli_notation_sync, test_cli_view, test_notation_validate_gives_typed_errors, test_palette_validation_is_typed y test_palette_cli_sync_writes_the_store_document) no se portan enteras: su parte de CLI tiene su equivalente en las filas K, que ya citan tests/visual/test_cli.py de IR. Pero dos de ellas también prueban la validación tipada sin la CLI, y esa parte sí se porta (precisión e): test_notation_validate_gives_typed_errors (load_notation lanza el error tipado, 7 casos) y test_palette_validation_is_typed (check_palette(PaletteSpec.model_validate(raw)) lanza el error tipado con su mensaje, 6 casos). Quedan 42 pruebas a portar. Las que usan un store (fixture store de test_notation.py) crean el suyo con sldb.api.init_store(tmp_path), como hace spec2viz, nunca sobre un store real; (3) las comparaciones «valida igual»: cada una de las 8 notaciones copiadas carga y valida con sldb y su contenido modelado es igual al de la builtin de sldb del mismo nombre, y la paleta default copiada es igual a la builtin default de sldb; (4) actualizar en la sección «Acreditación (IR13)» de docs/spec2viz/matriz-de-cobertura.md las filas SV-A17, SV-E02, SV-H01, SV-H02, SV-H03, SV-H04, SV-H05, SV-H06, SV-J06, SV-K18, SV-K19, SV-K20, SV-K22, SV-K23, SV-K24 y SV-K25, y el resumen de cumplidas/abiertas; (5) anotar en docs/spec2viz/acta-de-retiro.md la nueva salida de specir retirement check; (6) acreditar en «Acreditación (IR13)» SV-G08 y SV-I02, cuyo único pendiente era el label_key de sldb con '_' (nota 20261115-214942). sldb lo arregló en 06dbcf02 y task-quitar-el-xfail-obsoleto-de-label-key-en-test-catalog-tras-el-arreglo-de-sldb-06dbcf02 quitó el xfail: SV-G08 queda cumplida citando tests/visual/test_catalog.py (test_label_key_of_sldb_is_the_template_s_norm_key y test_label_key_of_sldb_splits_underscores_like_norm_key, sin xfail), y SV-I02 queda cumplida porque dependía solo de SV-G08. También se actualizan las menciones de label_key en el acta. Fuera: cambiar código de sldb o de spec2viz; implementar notaciones, paletas o vistas en specIR (son de sldb); las filas SV-K09, SV-K16, SV-K21, SV-K26 y SV-K29, que esperan cambios de sldb (nota 20261115-192054); la parte G5 de SV-A17 (store spec2viz/.sldb, desk de spec2viz); cambiar modos o condiciones de retiro de IR07; declarar el retiro.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las pruebas importan de sldb solo sldb.api (sldb.api.notations exporta resolve_view, render_template, render_keyword, flatten, fragments_of, lookup, ViewError y la sincronización de notaciones y paletas). Lo que sldb.api todavía no exporta (load_notation, builtin_notations, DEFAULT_NOTATIONS, NotationSpec, load_palette, check_palette, contrast, PaletteSpec, resolve_style y los errores de sldb.notations) se toma de src/specir/visual/notation_style.py, el único módulo de specIR autorizado a importar sldb.notations (tests/test_imports.py): se agregan ahí como reexportaciones los nombres que falten, sin definir nada nuevo, y se actualiza su docstring y __all__. ViewDoc se toma de sldb.api si sldb lo exporta; si no, la fila SV-A17 queda abierta diciendo que falta exportarlo y se pide a sldb con deskops message send --to sldb. Cuando un caso portado no pasa contra sldb (otra clase de error, otro mensaje, otro resultado) o una comparación «valida igual» encuentra diferencias, no se ajusta la expectativa para que pase: el caso se marca pytest.mark.xfail(strict=True) con la diferencia en reason, la fila queda abierta con esa diferencia en «lo que falta», y se envía una nota al desk de sldb con deskops message send --to sldb --root . citando la prueba. Una fila pasa a cumplida solo si todas sus pruebas citadas pasan sin xfail; las filas K dependientes se acreditan citando tests/visual/test_cli.py cuando todas las filas de las que dependen quedan cumplidas, y si no, siguen abiertas. Archivos: tests/visual/test_notations_parity.py (nuevo), tests/visual/fixtures/spec2viz-notations/ (nuevo), src/specir/visual/notation_style.py, docs/spec2viz/matriz-de-cobertura.md, docs/spec2viz/acta-de-retiro.md. Comandos desde la raíz de IR con TMPDIR=/dev/shm y el .venv del repo. Precisiones (preflight-1): (a) Las comparaciones «valida igual» son 9 casos: uno por cada notación copiada (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence) frente a la builtin de sldb del mismo nombre, y uno para la paleta default; con pytest.mark.parametrize cuentan como 9 pruebas. (b) Correspondencia prueba→fila, que es la que se cita en «Acreditación (IR13)»: SV-A17 ← las 3 de test_view_doc.py; SV-H01 ← de test_notation.py, test_builtins_load_and_cover_every_diagram_type, test_wildcard_link_and_free_relations, test_uml_class_notation_matches_the_class_spec_vocabulary, test_statechart_nests_contains_and_marks_the_initial_state, test_minimal_notation_defaults, test_invalid_notations_are_rejected, test_free_relation_diagram_types_accept_any_relation y test_load_notation_from_path_and_unknown_name; SV-E02 ← test_notation_sync_writes_docs_and_edges, test_notation_sync_is_idempotent_and_prunes, test_notation_naming_an_unregistered_model_is_reported y test_wildcard_link_leaves_no_dangling_relation_type de test_notation.py, más test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend y test_unstyled_notation_writes_no_palette_and_no_style de test_style_palette.py; SV-H02 ← las 8 comparaciones de notaciones y test_builtin_notations_still_validate_and_are_unstyled; SV-H03 ← las 10 no CLI de test_notation_view.py, las 2 de test_view_contract_resolved.py y test_resolve_documents_is_public_and_filters_relations; SV-H04 ← test_new_builtin_shapes_are_accepted, test_default_palette_is_accessible_and_distinguishable_without_colour, test_color_pair_is_validated_typed y test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not; SV-H05 ← la comparación de la paleta default; SV-H06 ← test_precedence_glyph_over_spec_over_palette, test_spec_style_kinds_are_validated_typed, test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec, test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched y test_mermaid_takes_the_light_side_of_a_spec_pair (las dos de mermaid se portan contra el renderer de specIR, specir.visual, que usa la precedencia de sldb). Son 40 pruebas portadas. (c) Filas K dependientes, según la columna «lo que falta» de la matriz: SV-J06 ← SV-H02 y SV-H05; SV-K19 ← SV-H02; SV-K20 ← SV-E02; SV-K22 ← SV-H03; SV-K24 ← SV-H05; SV-K25 ← SV-E02; SV-K18 ← SV-K19, K20, K21 y K22; SV-K23 ← SV-K24, K25 y K26. SV-K21 y SV-K26 están fuera de alcance (esperan un comando de sldb), así que SV-K18 y SV-K23 siguen abiertas en esta tarea; solo se actualiza su texto de «lo que falta». (d) Si una prueba de una fila no puede pasar (por ejemplo, si sldb.api no exporta ViewDoc), solo esa fila queda abierta; el resto de las pruebas y filas se portan y acreditan igual. Precisiones (corrección, ciclo 1): (e) Se portan, sin la invocación a la CLI, las aserciones de validación tipada de dos pruebas que antes se excluían enteras. (e1) test_notation_load_gives_typed_errors sale de test_notation_validate_gives_typed_errors de test_style_palette.py: los mismos 7 casos de parametrize (mutación sobre STYLED y clase de error esperada), con pytest.raises(error) sobre load_notation(path), y sin CliRunner. (e2) test_palette_check_is_typed sale de test_palette_validation_is_typed: los mismos 6 casos (mutación sobre la paleta default copiada en tests/visual/fixtures/spec2viz-notations/, clase de error y patrón de match), con pytest.raises(error, match=message) sobre check_palette(PaletteSpec.model_validate(raw)), y sin CliRunner. El docstring de cada una cita la prueba de origen y dice «parte no CLI». Las clases de error son las de sldb (vía notation_style), y si una no coincide se aplica la regla de xfail estricto más la nota a sldb. (f) Totales: 42 pruebas portadas más 9 comparaciones, o sea 51 funciones de prueba. Con la expansión de parametrize, el recuento de pytest lo informa el ejecutor. (g) Correspondencia nueva: SV-H01 suma test_notation_load_gives_typed_errors (validación de notaciones), y SV-H04 suma test_palette_check_is_typed. Una fila sigue cumplida solo si también pasan, sin xfail, las pruebas sumadas. SV-G08 y SV-I02 se acreditan según el punto (6) del scope, solo si test_catalog.py pasa sin xfailed ni xpassed para las dos pruebas de label_key. (h) Este es el ciclo de corrección 1. El trabajo del intento 1 (sin commitear) se conserva y se completa, y no se rehace: se agregan las 2 pruebas, se actualizan las filas SV-H01, SV-H04, SV-G08 y SV-I02 de «Acreditación (IR13)», el resumen de la matriz si cambia, y el acta con la nueva salida de specir retirement check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_notations_parity.py sale con rc 0 y tiene las 42 pruebas portadas (40, más test_notation_load_gives_typed_errors y test_palette_check_is_typed, con sus 7 y 6 casos) más las 9 comparaciones «valida igual» (passed o xfailed estricto, ninguna skipped).
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider -rxX tests/visual/test_catalog.py sale con rc 0, sin xfailed ni xpassed para las pruebas de label_key (respaldo de SV-G08 y SV-I02).
- grep -rnE '^(from|import) spec2viz' tests/visual/test_notations_parity.py no encuentra nada, y grep -rnE 'from sldb\.(notations|models|store|core)' tests/visual/test_notations_parity.py tampoco.
- timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb lista como no acreditadas solo filas que siguen abiertas en la matriz con su motivo, y ninguna de las filas que la matriz da por cumplidas; su salida queda en docs/spec2viz/acta-de-retiro.md.
- Suite completa una vez, bajo flock /dev/shm/sldb1-tests.lock, con el comando SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

tests/visual/test_notations_parity.py existe y pasa (rc 0) contra sldb sin importar spec2viz; cada una de las 16 filas listadas en el scope está, en «Acreditación (IR13)», como cumplida citando una prueba que pasa, o como abierta con la diferencia concreta y la referencia de la nota enviada a sldb; el resumen de la matriz y el acta reflejan la nueva salida de specir retirement check; la suite completa pasa.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

FILE:desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas
status: active
summary: Cómo se acredita la cobertura de una capacidad de spec2viz.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: la paridad con spec2viz se demuestra con sus pruebas

## What

_Define the context or guardrail this pill carries._

Una capacidad de spec2viz se considera cubierta solo cuando la prueba o golden correspondiente de spec2viz pasa contra specIR, o cuando su fila de la matriz de cobertura declara un reemplazo con una prueba equivalente que pasa.

## Why

_Explain why this context matters for safe execution._

El objetivo es retirar spec2viz; declarar paridad sin prueba dejaría funcionalidades perdidas al retirarlo.

## When

_Describe when an agent should apply this pill._

En toda tarea que migre o reemplace una capacidad de spec2viz, y al evaluar el gate de retiro.

## Where

_Name the files, surfaces, or scope this pill applies to._

tests/visual/ en specIR; como referencia de solo lectura, spec2viz/tests/ y la matriz docs/spec2viz/matriz-de-cobertura.md.

## How

_Describe the correct way to apply this guidance._

Portar los fixtures y golden de spec2viz a tests/ de specIR y ejecutarlos; registrar en la matriz, por fila, la prueba que acredita la cobertura.

## How Not

_Describe the shortcut or failure mode to avoid._

No declarar una fila como cubierta porque otra herramienta la sustituya de hecho; no descartar una capacidad por falta de uso; no modificar un golden para que la prueba pase.

FILE:desk/atoms/atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:35Z'
  authority: generated
  via: create_document
id: atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
title: specIR reemplaza a spec2viz y cubre todas sus funciones
five_wh_one_plus: when
tags:
- system:specir
- system:spec2viz
- topic:migracion
---

# specIR reemplaza a spec2viz y cubre todas sus funciones

## Answer

spec2viz nació aparte porque SLDB no tenía grafos; ahora los tiene. specIR incorporará la capa visual y debe cubrir todas las funcionalidades de spec2viz; cuando las cubra, spec2viz se retira. Ninguna funcionalidad se da por descartada porque otra herramienta la sustituya de hecho: cada una se cubre migrándola tal cual, reemplazándola por otra arquitectura o experiencia con resultado equivalente, o exponiendo desde specIR lo que ya vive en SLDB. En los tres casos specIR responde por el camino de retiro. No es un consumidor permanente de spec2viz. Decisión del dueño del proyecto, 2026-11-11.

FILE:desk/atoms/atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:36Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
title: El vocabulario visual y el resolvedor de vistas ya viven en SLDB
five_wh_one_plus: where
tags:
- system:specir
- system:sldb
- system:spec2viz
- topic:vistas
- layer:modelo
provenance: ../sldb-astryx/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/dag.yaml
---

# El vocabulario visual y el resolvedor de vistas ya viven en SLDB

## Answer

Desde el plan absorber-spec2viz-y-modelos-ui de SLDB (entregado el 2026-11-07), los modelos SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb/src/sldb/models/notation/, las notaciones y paletas builtin en sldb/src/sldb/notations/, y el resolvedor de vistas y proyecciones en sldb/src/sldb/api/notations/. Un alias en sldb/src/sldb/api/model_registry/model_reference.py resuelve las referencias antiguas spec2viz.sldb_models. specIR usa esas piezas desde SLDB y no las redefine. En spec2viz quedan, sin equivalente en SLDB, la autoría de specs YAML, los compiladores, los renderizadores, el catálogo y la sincronización de specs al store.

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:tests/visual/test_notations_parity.py
"""spec2viz's notation, palette and view tests, ported to run against sldb (IR13e).

The notations, palettes, the view contract (`resolve_view`) and its sync to the store are sldb's
(D1, D3): this file runs, against sldb and never against spec2viz, the cases of spec2viz's
`tests/test_view_doc.py` (3), `test_notation.py` (12 of 14), `test_notation_view.py` (10 of 11),
`test_view_contract_resolved.py` (2) and `test_style_palette.py` (13 of 16), revision b624b75.
The 6 tests that invoke spec2viz's CLI (`test_cli_list_and_validate`, `test_cli_notation_sync`,
`test_cli_view`, `test_notation_validate_gives_typed_errors`, `test_palette_validation_is_typed`,
`test_palette_cli_sync_writes_the_store_document`) are not ported here: their equivalent are rows
SV-K of the coverage matrix, credited by `tests/visual/test_cli.py`.

Each ported test names, in its docstring, the spec2viz test it comes from. Only the imports
change: the store, the sync and the view resolver come from `sldb.api` (`sldb.api.notations`);
what `sldb.api` does not export yet (`load_notation`, `NotationSpec`, `load_palette`, `PaletteSpec`,
`check_palette`, `contrast`, `resolve_color`, `resolve_style`, `SHAPES`, `DiagramType`,
`DEFAULT_NOTATIONS`, `builtin_notations` and the typed errors) is taken from
`specir.visual.notation_style`, the one module of specIR allowed to reach `sldb.notations`; the
mermaid and PlantUML renderers are specIR's (`specir.visual.renderers`), over sldb's spec loader.

The fixtures are spec2viz's, copied: its 8 builtin notations and its `default` palette in
`fixtures/spec2viz-notations/` (revision b624b75), its specs in `fixtures/spec2viz/` and its
catalog (`docs/architecture/vistas.yml` with its specs) in `fixtures/catalog/`.

The 9 «valida igual» comparisons check that each notation and the palette copied from spec2viz
load and validate with sldb, and that their `model_dump()` equals that of sldb's builtin of the
same name."""

from __future__ import annotations

import copy
import re
import shutil
from pathlib import Path

import pytest
import sldb.api as sldb_api
import yaml
from sldb.api import ViewDoc
from sldb.api.notations import (
    NotationSync,
    SpecSync,
    ViewError,
    flatten,
    fragments_of,
    lookup,
    render_keyword,
    render_template,
    resolve_documents,
    resolve_view,
)
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

from specir.visual.compilers import compile_ir
from specir.visual.notation_style import (
    DEFAULT_NOTATIONS,
    SHAPES,
    DiagramType,
    InvalidColorError,
    NotationSpec,
    UnknownIconError,
    ValidationError,
    builtin_notations,
    contrast,
    load_notation,
    load_palette,
    resolve_color,
    resolve_style,
)
from specir.visual.renderers.mermaid import MermaidRenderer
from specir.visual.renderers.plantuml import PlantUMLRenderer

HERE = Path(__file__).parent
NOTATION_COPIES = HERE / "fixtures" / "spec2viz-notations"
#: spec2viz's repository as copied into IR: its `tests/fixtures/` and `docs/architecture/spec2viz/`.
SPEC2VIZ = HERE / "fixtures" / "spec2viz"
#: spec2viz's catalog (`docs/architecture/vistas.yml` and the specs it lists), as copied into IR.
CATALOG = HERE / "fixtures" / "catalog"
FIXTURES = SPEC2VIZ / "tests" / "fixtures"
SPEC2VIZ_NOTATIONS = ("activity", "component", "component-view-matrix", "deployment", "reflection", "statechart", "uml-class", "uml-sequence")


def _front(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])


# ==================================================================================================
# «valida igual»: the notations and the palette copied from spec2viz against sldb's builtins
# ==================================================================================================

@pytest.mark.parametrize("name", SPEC2VIZ_NOTATIONS)
def test_spec2viz_notation_validates_the_same_as_the_sldb_builtin(name):
    """«valida igual»: the notation copied from spec2viz loads and validates with sldb, and its
    content equals that of sldb's builtin of the same name."""
    copied = load_notation(NOTATION_COPIES / "notations" / f"{name}.yml")
    assert name in builtin_notations()
    assert copied.model_dump() == load_notation(name).model_dump()


def test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin():
    """«valida igual»: the `default` palette copied from spec2viz loads and validates with sldb
    (`load_palette` runs `check_palette`), and its content equals that of sldb's builtin `default`."""
    copied = load_palette(NOTATION_COPIES / "palettes" / "default.yml")
    assert copied.model_dump() == load_palette("default").model_dump()


# ==================================================================================================
# spec2viz tests/test_view_doc.py
# ==================================================================================================

VIEW_BASE = {"id": "atoms-by-task", "name": "atoms-by-task", "title": "Atoms by task"}


def test_defaults_and_shape():
    """spec2viz tests/test_view_doc.py::test_defaults_and_shape."""
    v = ViewDoc.model_validate(VIEW_BASE)
    assert v.nodes == [] and v.relations == [] and v.direction == "both" and v.notation == "" and v.layout == {}
    v = ViewDoc.model_validate({**VIEW_BASE, "nodes": [{"model": "TaskDoc"}, {"model": "AtomDoc", "where": 'five_wh_one_plus = "why"'}],
                                "relations": ["references"], "direction": "outgoing", "notation": "NotationDoc:component",
                                "layout": {"kind": "graph", "style": "rings", "ring_field": "status"}})
    assert v.nodes == [{"model": "TaskDoc", "where": ""}, {"model": "AtomDoc", "where": 'five_wh_one_plus = "why"'}]
    assert v.layout["style"] == "rings"


@pytest.mark.parametrize("changes, message", [
    ({"direction": "up"}, "direction"),
    ({"nodes": [{"where": "x"}]}, "needs a model"),
    ({"nodes": [{"model": "A", "id": "SpecNodeDoc:x"}]}, "only take model and where"),
    ({"layout": {"style": "force"}}, "layout.style"),
])
def test_invalid(changes, message):
    """spec2viz tests/test_view_doc.py::test_invalid."""
    with pytest.raises(Exception, match=message):
        ViewDoc.model_validate({**VIEW_BASE, **changes})


def test_view_doc_in_a_store_references_its_notation(tmp_path):
    """spec2viz tests/test_view_doc.py::test_view_doc_in_a_store_references_its_notation."""
    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    NotationSync(store).sync("component")
    payload = {**VIEW_BASE, "nodes": [{"model": "SpecNodeDoc", "where": 'kind = "entry"'}], "relations": ["uses"],
               "direction": "both", "notation": "NotationDoc:component", "layout": {"style": "layered"}, "description": "entry points"}
    sldb_api.create_document(store, "ViewDoc", tmp_path / "sldb" / "views" / "atoms-by-task.md", payload, name="atoms-by-task")
    sldb_api.rebuild_edges(store)
    front = _front(tmp_path / "sldb" / "views" / "atoms-by-task.md")
    assert front["nodes"] == [{"model": "SpecNodeDoc", "where": 'kind = "entry"'}] and front["notation"] == "NotationDoc:component"
    targets = {r.target for r in sldb_api.edges_from(store, "ViewDoc:atoms-by-task") if r.relation == "references"}
    assert targets == {"sldb://document/NotationDoc:component"}
    assert sldb_api.check_edges(store).errors == []


# ==================================================================================================
# spec2viz tests/test_notation.py
# ==================================================================================================

MINIMAL = {
    "name": "mini",
    "diagram_type": "class",
    "glyphs": [{"id": "box", "model": "SpecNodeDoc", "shape": "class-box"}],
    "links": [{"id": "inh", "relation": "inheritance", "target_end": "hollow-triangle"}],
}


def _with(**changes) -> dict:
    raw = yaml.safe_load(yaml.safe_dump(MINIMAL))
    raw.update(changes)
    return raw


def test_builtins_load_and_cover_every_diagram_type():
    """spec2viz tests/test_notation.py::test_builtins_load_and_cover_every_diagram_type."""
    names = set(builtin_notations())
    assert set(DEFAULT_NOTATIONS.values()) == names and set(DEFAULT_NOTATIONS) == {t.value for t in DiagramType}
    for name in names:
        spec = load_notation(name)
        assert spec.name == name and spec.glyphs and DEFAULT_NOTATIONS[spec.diagram_type] == name


def test_wildcard_link_and_free_relations():
    """spec2viz tests/test_notation.py::test_wildcard_link_and_free_relations."""
    spec = NotationSpec.model_validate(_with(diagram_type="component", links=[{"id": "any", "relation": "*"}, {"id": "c", "relation": "contains", "draw": "nest"}]))
    assert spec.relations == ["contains"]
    with pytest.raises(Exception, match="never emits"):
        NotationSpec.model_validate(_with(links=[{"id": "l", "relation": "uses"}]))
    with pytest.raises(Exception, match="vocabulary token"):
        NotationSpec.model_validate(_with(links=[{"id": "l", "relation": "Uses It"}]))


def test_uml_class_notation_matches_the_class_spec_vocabulary():
    """spec2viz tests/test_notation.py::test_uml_class_notation_matches_the_class_spec_vocabulary."""
    spec = load_notation("uml-class")
    assert spec.relations == ["contains", "inheritance", "realization", "composition", "aggregation", "association", "dependency"]
    assert [g.id for g in spec.glyphs][-1] == "class" and spec.glyphs[-1].where == ""
    assert spec.glyphs[0].id == "package" and spec.glyphs[0].shape == "package" and spec.glyphs[0].where == 'collection = "packages"'
    assert spec.glyphs[1].where == 'kind = "interface"' and spec.glyphs[1].keyword == "«interface»"
    assert {l.id: l.draw for l in spec.links}["contains"] == "nest"
    assert {l.id: (l.draw, l.line, l.source_end, l.target_end) for l in spec.links}["composition"] == ("line", "solid", "filled-diamond", "none")


def test_statechart_nests_contains_and_marks_the_initial_state():
    """spec2viz tests/test_notation.py::test_statechart_nests_contains_and_marks_the_initial_state."""
    spec = load_notation("statechart")
    links = {l.relation: l for l in spec.links}
    assert links["contains"].draw == "nest" and links["transitions_to"].draw == "line"
    assert spec.markers[0].model_dump() == {"id": "initial", "shape": "filled-circle", "model": "SpecNodeDoc", "where": "has(initial)"}
    assert spec.glyphs[0].where == "nonempty(contains)"


def test_minimal_notation_defaults():
    """spec2viz tests/test_notation.py::test_minimal_notation_defaults."""
    spec = NotationSpec.model_validate(MINIMAL)
    assert spec.level == "types" and spec.layout == {"kind": "graph"} and spec.projection == "all"
    assert spec.links[0].draw == "line" and spec.links[0].line == "solid" and spec.links[0].source_end == "none"
    assert spec.models == ["SpecNodeDoc"] and spec.relations == ["inheritance"]


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"name": "Mini Notation"}, "notation name"),
        pytest.param(
            {"diagram_type": "mindmap"}, "not a spec2viz diagram type",
            marks=pytest.mark.xfail(strict=True, reason=(
                "sldb rejects the unknown diagram_type with another message: \"diagram_type 'mindmap' is not a "
                "valid diagram type\" (sldb/notations/notation_spec.py), where spec2viz said \"not a spec2viz "
                "diagram type\"; reported to sldb's desk")),
        ),
        ({"level": "all"}, "level"),
        ({"layout": {"kind": "force"}}, "layout.kind"),
        ({"layout": {"kind": "graph", "direction": "UP"}}, "layout.direction"),
        ({"glyphs": []}, "glyphs"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x", "where": 'kind = "a"'}]}, "no default glyph"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x"}, {"id": "a", "model": "SpecNodeDoc", "shape": "y"}]}, "more than once"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x", "where": "kind = = 1"}]}, "does not parse"),
        ({"links": [{"id": "l", "relation": "uses"}]}, "never emits"),
        ({"links": [{"id": "l", "relation": "inheritance", "draw": "curve"}]}, "draw"),
        ({"links": [{"id": "l", "relation": "inheritance", "target_end": "spear"}]}, "terminal"),
        ({"links": [{"id": "l", "relation": "inheritance", "model": "AssocDoc"}]}, "declares no ends"),
        ({"links": [{"id": "l", "relation": "inheritance"}, {"id": "m", "relation": "inheritance"}]}, "more than one link"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x", "colour": "red"}]}, "colour"),
    ],
)
def test_invalid_notations_are_rejected(changes, message):
    """spec2viz tests/test_notation.py::test_invalid_notations_are_rejected."""
    with pytest.raises(Exception) as excinfo:
        NotationSpec.model_validate(_with(**changes))
    assert message in str(excinfo.value)


def test_free_relation_diagram_types_accept_any_relation():
    """spec2viz tests/test_notation.py::test_free_relation_diagram_types_accept_any_relation."""
    spec = NotationSpec.model_validate(_with(diagram_type="component", links=[{"id": "l", "relation": "loads_path"}]))
    assert spec.relations == ["loads_path"]


def test_load_notation_from_path_and_unknown_name(tmp_path):
    """spec2viz tests/test_notation.py::test_load_notation_from_path_and_unknown_name."""
    path = tmp_path / "mine.yml"
    path.write_text(yaml.safe_dump(MINIMAL), encoding="utf-8")
    assert load_notation(path).name == "mini"
    with pytest.raises(ValidationError, match="unknown notation"):
        load_notation("nope")
    path.write_text("- not\n- a mapping\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="a mapping"):
        load_notation(path)


@pytest.fixture
def store(tmp_path):
    sldb_api.init_store(tmp_path)
    return tmp_path / ".sldb"


def test_notation_sync_writes_docs_and_edges(store):
    """spec2viz tests/test_notation.py::test_notation_sync_writes_docs_and_edges."""
    report = NotationSync(store).sync("statechart")
    assert sorted(report.created) == [
        "GlyphDoc:statechart.composite", "GlyphDoc:statechart.state",
        "LinkDoc:statechart.substate", "LinkDoc:statechart.transition",
        "NotationDoc:statechart",
    ]
    assert report.relation_types_added == ["transitions_to"]  # `contains` es builtin
    assert report.unresolved == [] and report.edge_errors == []
    root = store.parent
    assert (root / "sldb" / "notations" / "statechart" / "notation.md").exists()
    assert (root / "sldb" / "notations" / "statechart" / "glyphs" / "composite.md").exists()
    assert (root / "sldb" / "notations" / "statechart" / "links" / "transition.md").exists()

    notation = _front(root / "sldb" / "notations" / "statechart" / "notation.md")
    assert notation["layout"] == {"kind": "graph", "direction": "LR"} and notation["markers"][0]["where"] == "has(initial)"
    assert notation["glyphs"] == ["GlyphDoc:statechart.composite", "GlyphDoc:statechart.state"]

    rels = sorted((r.relation, r.target) for r in sldb_api.edges_from(store, "NotationDoc:statechart") if r.relation == "references")
    assert ("references", "sldb://document/GlyphDoc:statechart.state") in rels
    assert ("references", "sldb://document/LinkDoc:statechart.transition") in rels
    link_rels = {(r.relation, r.target) for r in sldb_api.edges_from(store, "LinkDoc:statechart.transition")}
    assert ("references", "sldb://relation_type/transitions_to") in link_rels
    assert ("references", "sldb://document/NotationDoc:statechart") in link_rels


def test_notation_sync_is_idempotent_and_prunes(store, tmp_path):
    """spec2viz tests/test_notation.py::test_notation_sync_is_idempotent_and_prunes."""
    sync = NotationSync(store)
    path = tmp_path / "mini.yml"
    path.write_text(yaml.safe_dump(MINIMAL), encoding="utf-8")
    first = sync.sync(path)
    again = sync.sync(path)
    assert first.created and again.created == [] and len(again.updated) == 3 and again.deleted == []

    smaller = yaml.safe_load(yaml.safe_dump(MINIMAL))
    smaller["links"] = []
    path.write_text(yaml.safe_dump(smaller), encoding="utf-8")
    pruned = sync.sync(path)
    assert pruned.deleted == ["LinkDoc:mini.inh"] and not sldb_api.doc_exists(store, "LinkDoc/mini.inh")


def test_notation_naming_an_unregistered_model_is_reported(store, tmp_path):
    """spec2viz tests/test_notation.py::test_notation_naming_an_unregistered_model_is_reported."""
    path = tmp_path / "other.yml"
    path.write_text(yaml.safe_dump(_with(name="other", glyphs=[{"id": "b", "model": "ClassDoc", "shape": "box"}])), encoding="utf-8")
    report = NotationSync(store).sync(path)
    assert report.unresolved == ["notation other: model 'ClassDoc' is not registered in the store"]


def test_wildcard_link_leaves_no_dangling_relation_type(store):
    """spec2viz tests/test_notation.py::test_wildcard_link_leaves_no_dangling_relation_type."""
    report = NotationSync(store).sync("component")
    assert report.unresolved == [] and report.edge_errors == []
    link = _front(store.parent / "sldb" / "notations" / "component" / "links" / "relation.md")
    assert link["relation"] == "*" and link["relation_type"] == ""
    targets = {r.target for r in sldb_api.edges_from(store, "LinkDoc:component.relation") if r.relation == "references"}
    assert targets == {"sldb://document/NotationDoc:component"}


# ==================================================================================================
# spec2viz tests/test_notation_view.py
# ==================================================================================================

def _in_project(tmp_path: Path, rel: str, source_root: Path = SPEC2VIZ) -> Path:
    """Copy of a spec of spec2viz's repo (or of vistas.yml with every spec it lists) inside the
    temporary project, at the same relative path (spec2viz's helper, over the copies in IR)."""
    source = source_root / rel
    if source.name == "vistas.yml":
        shutil.copytree(source.parent, tmp_path / rel.rsplit("/", 1)[0], dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("sldb", "*.md", "*.html", "*.svg", "*.puml", "*.mmd"))
    else:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, tmp_path / rel)
    return tmp_path / rel


CLASSES = {
    "id": "shapes", "title": "Shapes", "type": "class", "version": "1",
    "data": {
        "classes": {
            "Shape": {"kind": "interface", "methods": [{"name": "area", "returns": "float"}]},
            "Base": {"kind": "abstract", "attributes": [{"name": "name", "type": "str"}]},
            "Circle": {"label": "Circle", "attributes": [{"name": "r", "type": "float"}], "methods": [{"name": "area", "returns": "float"}]},
        },
        "relations": [
            {"from": "Circle", "to": "Base", "relation": "inheritance"},
            {"from": "Base", "to": "Shape", "relation": "realization"},
            {"from": "Circle", "to": "Shape", "relation": "composition", "label": "parts", "from_multiplicity": "1", "to_multiplicity": "1..*"},
        ],
    },
}
MACHINE = {
    "id": "door", "title": "Door", "type": "state", "version": "1",
    "data": {
        "entity": "Door", "initial": "closed",
        "states": [
            {"id": "closed", "label": "Closed"},
            {"id": "open", "label": "Open", "contains": ["ajar", "wide"]},
            {"id": "ajar", "label": "Ajar"},
            {"id": "wide", "label": "Wide open"},
        ],
        "transitions": [
            {"from": "closed", "to": "open", "on": "push", "guard": "unlocked"},
            {"from": "open", "to": "closed", "on": "pull"},
            {"from": "wide", "to": "closed", "on": "slam"},  # cruza el borde del compuesto
        ],
    },
}


@pytest.fixture
def project(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "shapes.yml").write_text(yaml.safe_dump(CLASSES), encoding="utf-8")
    (tmp_path / "docs" / "door.yml").write_text(yaml.safe_dump(MACHINE), encoding="utf-8")
    return tmp_path


def test_pure_helpers():
    """spec2viz tests/test_notation_view.py::test_pure_helpers."""
    payload = {"title": "A", "kind": "", "data": {"initial": True, "attributes": [1], "title": "shadow"}}
    assert flatten(payload)["initial"] is True and flatten(payload)["title"] == "A"
    assert lookup(payload, "data.attributes") == [1] and lookup(payload, "data.nope.x") is None
    assert render_template("{title} <{kind}> {missing} {data.initial}", payload) == "A <> True"


def test_class_view_picks_glyphs_by_where_and_links_by_relation(project):
    """spec2viz tests/test_notation_view.py::test_class_view_picks_glyphs_by_where_and_links_by_relation.

    spec2viz asserted the multiplicities of the composition only when the installed sldb stored
    relation attributes (`relation_doc_has_attributes()`, sldb >= 0.1.11); sldb stores them, so
    that branch is the one that runs here."""
    store = project / ".sldb"
    SpecSync(store).sync(project / "docs" / "shapes.yml")
    view = resolve_view(store, "shapes")
    assert view["notation"] == "NotationDoc:uml-class" and view["layout"] == {"kind": "graph", "direction": "TB"}
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["Shape"]["glyph"] == "GlyphDoc:uml-class.interface" and nodes["Shape"]["keyword"] == "«interface»"
    assert nodes["Base"]["glyph"] == "GlyphDoc:uml-class.abstract" and nodes["Base"]["label_style"] == "italic"
    assert nodes["Circle"]["glyph"] == "GlyphDoc:uml-class.class" and nodes["Circle"]["label"] == "Circle"
    assert [c["path"] for c in nodes["Circle"]["compartments"]] == ["data.attributes", "data.methods"]
    assert nodes["Circle"]["compartments"][0]["items"] == [{"name": "r", "type": "float"}]
    assert [c["path"] for c in nodes["Shape"]["compartments"]] == ["data.methods"]  # sin atributos no hay compartimento
    links = {(l["source"].split(".")[-1], l["target"].split(".")[-1]): l for l in view["links"]}
    assert links[("Circle", "Base")]["target_end"] == "hollow-triangle" and links[("Circle", "Base")]["line"] == "solid"
    assert links[("Base", "Shape")]["line"] == "dashed"
    assert links[("Circle", "Shape")]["source_end"] == "filled-diamond" and links[("Circle", "Shape")]["label"] == "parts"
    assert all(l["draw"] == "line" and l["doc"].startswith("RelationDoc:shapes.") for l in view["links"])
    assert view["skipped"] == [] and view["fragments"] == []
    composition = links[("Circle", "Shape")]
    assert composition["data"] == {"from_multiplicity": "1", "to_multiplicity": "1..*", "label": "parts"}
    assert (composition["source_label"], composition["target_label"]) == ("1", "1..*")


def test_state_view_nests_contains_and_marks_initial(project):
    """spec2viz tests/test_notation_view.py::test_state_view_nests_contains_and_marks_initial."""
    store = project / ".sldb"
    SpecSync(store).sync(project / "docs" / "door.yml")
    view = resolve_view(store, "SpecDoc:door")
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["open"]["glyph"] == "GlyphDoc:statechart.composite" and nodes["ajar"]["glyph"] == "GlyphDoc:statechart.state"
    assert nodes["closed"]["markers"] == [{"id": "initial", "shape": "filled-circle"}] and nodes["open"]["markers"] == []
    nests = sorted((l["source"].split(".")[-1], l["target"].split(".")[-1]) for l in view["links"] if l["draw"] == "nest")
    assert nests == [("open", "ajar"), ("open", "wide")] and all(l["doc"] is None for l in view["links"] if l["draw"] == "nest")
    lines = {(l["source"].split(".")[-1], l["target"].split(".")[-1]): l["label"] for l in view["links"] if l["draw"] == "line"}
    assert lines == {("closed", "open"): "push [unlocked]", ("open", "closed"): "pull", ("wide", "closed"): "slam"}


def test_repo_pilot_with_a_composite_state_resolves_nest_and_a_crossing_transition(tmp_path):
    """spec2viz tests/test_notation_view.py::test_repo_pilot_with_a_composite_state_resolves_nest_and_a_crossing_transition."""
    sldb_api.init_store(tmp_path)
    SpecSync(tmp_path / ".sldb").sync(_in_project(tmp_path, "docs/architecture/spec2viz/state-diagram-sync-lifecycle.yml"))
    view = resolve_view(tmp_path / ".sldb", "state.diagram-sync-lifecycle")
    nests = sorted((l["source"].split(".")[-1], l["target"].split(".")[-1]) for l in view["links"] if l["draw"] == "nest")
    assert nests == [("syncing", "indexing"), ("syncing", "validating"), ("syncing", "writing")]
    crossing = [l for l in view["links"] if l["draw"] == "line" and l["source"].endswith(".validating") and l["target"].endswith(".failed")]
    assert len(crossing) == 1 and crossing[0]["label"] == "load() raises [spec invalid]"
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["syncing"]["glyph"] == "GlyphDoc:statechart.composite" and nodes["idle"]["markers"][0]["id"] == "initial"
    assert view["skipped"] == []


def test_fragments_group_consecutive_messages():
    """spec2viz tests/test_notation_view.py::test_fragments_group_consecutive_messages."""
    links = [
        {"order": 1, "data": {}}, {"order": 2, "data": {"group": "loop"}}, {"order": 3, "data": {"group": "loop"}},
        {"order": 4, "data": {"group": "alt"}}, {"order": 5, "data": {}}, {"order": 6, "data": {"group": "alt"}}, {"order": 0, "data": {"group": "x"}},
    ]
    assert fragments_of(links) == [
        {"label": "", "kind": "loop", "group": "loop", "orders": [2, 3]},
        {"label": "", "kind": "alt", "group": "alt", "orders": [4]},
        {"label": "", "kind": "alt", "group": "alt", "orders": [6]},
    ]
    assert fragments_of([{"order": 1, "data": {"group": "Loop for each spec"}}, {"order": 2, "data": {"group": "retries"}}]) == [
        {"label": "for each spec", "kind": "loop", "group": "Loop for each spec", "orders": [1]},
        {"label": "retries", "kind": "group", "group": "retries", "orders": [2]},
    ]


def test_repo_sequence_pilot_has_loop_and_alt_fragments(tmp_path):
    """spec2viz tests/test_notation_view.py::test_repo_sequence_pilot_has_loop_and_alt_fragments."""
    sldb_api.init_store(tmp_path)
    SpecSync(tmp_path / ".sldb").sync(_in_project(tmp_path, "docs/architecture/spec2viz/sequence-sync-pipeline.yml"))
    view = resolve_view(tmp_path / ".sldb", "sequence.sync-pipeline")
    kinds = [(f["kind"], f["label"]) for f in view["fragments"]]
    assert kinds == [("loop", "for each spec"), ("alt", "the diagram type has a notation"), ("loop", "for each spec")]
    loop = view["fragments"][0]
    by_order = {l["order"]: l for l in view["links"]}
    participants = {by_order[o][end].split(".")[-1] for o in loop["orders"] for end in ("source", "target")}
    assert len(participants) >= 3 and view["skipped"] == []


def test_view_errors(project):
    """spec2viz tests/test_notation_view.py::test_view_errors."""
    store = project / ".sldb"
    with pytest.raises(ViewError, match="not in the store"):
        resolve_view(store, "nope")
    SpecSync(store).sync(project / "docs" / "door.yml", notation="none")
    with pytest.raises(ViewError, match="has no notation"):
        resolve_view(store, "door")


def test_every_catalog_spec_resolves_under_its_builtin_notation(tmp_path):
    """spec2viz tests/test_notation_view.py::test_every_catalog_spec_resolves_under_its_builtin_notation.

    spec2viz's `docs/architecture/vistas.yml` and its specs, as copied into IR (`fixtures/catalog/`)."""
    from sldb.api.notations import sync_catalog

    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    reports = sync_catalog(SpecSync(store), _in_project(tmp_path, "docs/architecture/vistas.yml", CATALOG))
    assert len(reports) >= 9 and all(r.edge_errors == [] for r in reports)
    seen_types = set()
    for report in reports:
        view = resolve_view(store, report.spec_id)
        seen_types.add(view["diagram_type"])
        assert view["skipped"] == [], (report.spec_id, view["skipped"])
        assert view["nodes"] and all(n["glyph"] for n in view["nodes"])
    assert {"component", "sequence", "state", "activity", "class", "component_view_matrix"} <= seen_types
    spec_doc = next(d for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if str(d.model_name) == "SpecDoc" and d.name == "component.spec2viz-architecture")
    assert spec_doc.payload["category"] == "Arquitectura de Módulos" and spec_doc.payload["nav"] == "Módulos"


def test_component_wildcard_link_and_sequence_order(tmp_path):
    """spec2viz tests/test_notation_view.py::test_component_wildcard_link_and_sequence_order."""
    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    (tmp_path / "arq.yml").write_text(yaml.safe_dump({
        "id": "arq", "title": "Arq", "type": "component", "version": "1",
        "data": {"nodes": {"cli": {"label": "CLI", "kind": "entry", "contains": ["core"]}, "core": {"label": "Core"}, "db": {"label": "DB", "kind": "boundary"}},
                 "edges": [{"from": "core", "to": "db", "relation": "reads(sql)", "label": "rows"}, {"from": "cli", "to": "core", "relation": "uses"}]}}), encoding="utf-8")
    (tmp_path / "seq.yml").write_text(yaml.safe_dump({
        "id": "seq", "title": "Seq", "type": "sequence", "version": "1",
        "data": {"participants": [{"id": "U", "kind": "actor"}, {"id": "S", "kind": "component"}],
                 "messages": [{"from": "U", "to": "S", "message": "first"}, {"from": "S", "to": "U", "message": "second", "kind": "return"}, {"from": "U", "to": "S", "message": "third", "kind": "async"}]}}), encoding="utf-8")
    sync = SpecSync(store)
    sync.sync(tmp_path / "arq.yml")
    sync.sync(tmp_path / "seq.yml")

    arq = resolve_view(store, "arq")
    nodes = {n["element"]: n for n in arq["nodes"]}
    assert nodes["cli"]["glyph"] == "GlyphDoc:component.entry" and nodes["db"]["glyph"] == "GlyphDoc:component.boundary" and nodes["core"]["collection"] == "nodes"
    links = [(l["source"].split(".")[-1], l["target"].split(".")[-1], l["relation"], l["draw"], l["label"], l["order"]) for l in arq["links"]]
    assert links == [("cli", "core", "contains", "nest", "", 0), ("core", "db", "reads_sql", "line", "reads_sql rows", 1), ("cli", "core", "uses", "line", "uses", 2)]
    assert all(l["link"] == "LinkDoc:component.relation" for l in arq["links"] if l["draw"] == "line")

    seq = resolve_view(store, "seq")
    assert seq["layout"] == {"kind": "lanes", "direction": "LR"}
    assert [(l["order"], l["relation"], l["line"], l["target_end"], l["label"]) for l in seq["links"]] == [
        (1, "sends", "solid", "filled-arrow", "first"), (2, "returns", "dashed", "open-arrow", "second"), (3, "sends_async", "solid", "open-arrow", "third")]
    assert {n["element"]: n["glyph"].split(".")[-1] for n in seq["nodes"]} == {"U": "actor", "S": "participant"}


def test_activity_and_matrix_views(tmp_path):
    """spec2viz tests/test_notation_view.py::test_activity_and_matrix_views."""
    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    sync = SpecSync(store)
    sync.sync(_in_project(tmp_path, "docs/architecture/spec2viz/activity-render-error-handling.yml"))
    sync.sync(_in_project(tmp_path, "tests/fixtures/matrix.quotation-view.yml"))

    act = resolve_view(store, "activity.render-error-handling")
    glyphs = {n["element"]: n["glyph"].split(".")[-1] for n in act["nodes"]}
    assert glyphs["__initial"] == "start" and glyphs["receive_paths"] == "action" and glyphs["iterate_path"] == "decision"
    assert glyphs["try_render"] == "action" and glyphs["__final"] == "end" and glyphs["done"] == "action"
    start = next(n for n in act["nodes"] if n["element"] == "__initial")
    assert start["label"] == ""  # label: "" explicito en el glifo: sin rotulo
    branch = next(l for l in act["links"] if l["relation"] == "branch" and l["source"].endswith(".iterate_path") and l["target"].endswith(".try_render"))
    assert branch["label"] == "[has_next]" and act["skipped"] == []

    mat = resolve_view(store, "matrix.quotation-view")
    assert mat["layout"] == {"kind": "grid"}
    stages = [n for n in mat["nodes"] if n["collection"] == "stages"]
    assert [s["data"]["order"] for s in stages] == [1, 2, 3, 4, 5] and stages[0]["glyph"] == "GlyphDoc:component-view-matrix.stage"
    cells = [l for l in mat["links"] if l["draw"] == "cell"]
    nests = [l for l in mat["links"] if l["draw"] == "nest"]
    assert cells and nests and all(c["label"] == "quotation" for c in cells) and mat["skipped"] == []


# ==================================================================================================
# spec2viz tests/test_view_contract_resolved.py
# ==================================================================================================

PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_.]+\}")
CONTRACT_SPECS = [
    FIXTURES / "deployment.nested.yml", FIXTURES / "deployment.runtime.yml", FIXTURES / "activity.lanes.yml",
    FIXTURES / "component.styled.yml", SPEC2VIZ / "docs" / "architecture" / "spec2viz" / "state-diagram-sync-lifecycle.yml",
    SPEC2VIZ / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml", SPEC2VIZ / "docs" / "architecture" / "spec2viz" / "class-sldb-models.yml",
]


def _strings(value, path="view"):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _strings(v, f"{path}[{i}]")


def _unresolved(view):
    # `data` es el payload del documento tal cual; las plantillas resueltas son el resto
    return [(p, s) for p, s in _strings({k: v for k, v in view.items()}) if ".data." not in p and PLACEHOLDER.search(s)]


@pytest.mark.parametrize("spec", CONTRACT_SPECS, ids=lambda p: p.stem)
def test_no_placeholder_reaches_the_render_contract(tmp_path, spec):
    """spec2viz tests/test_view_contract_resolved.py::test_no_placeholder_reaches_the_render_contract."""
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    copy_ = shutil.copy(spec, tmp_path / "docs" / spec.name)
    report = SpecSync(tmp_path / ".sldb").sync(Path(copy_))
    view = resolve_view(tmp_path / ".sldb", report.spec_id)
    assert _unresolved(view) == []


def test_deployment_keyword_interpolates_kind_and_drops_when_empty(tmp_path):
    """spec2viz tests/test_view_contract_resolved.py::test_deployment_keyword_interpolates_kind_and_drops_when_empty."""
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    copy_ = shutil.copy(FIXTURES / "deployment.nested.yml", tmp_path / "docs" / "nested.yml")
    SpecSync(tmp_path / ".sldb").sync(Path(copy_))
    nodes = {n["element"]: n for n in resolve_view(tmp_path / ".sldb", "deployment.nested")["nodes"]}
    assert nodes["db"]["keyword"] == "«database»" and nodes["api_image"]["keyword"] == "«image»"
    assert render_keyword("«{kind}»", {"kind": ""}) == "" and render_keyword("«{kind}»", {}) == ""
    assert render_keyword("«interface»", {}) == "«interface»" and render_keyword("", {"kind": "x"}) == ""


# ==================================================================================================
# spec2viz tests/test_style_palette.py
# ==================================================================================================

STYLED = {
    "name": "infra", "title": "Infra", "diagram_type": "component", "layout": {"kind": "graph"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "kind": "database"},
        {"id": "api", "model": "SpecNodeDoc", "where": 'kind = "backend"', "shape": "box", "fill": "#fafafa"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [{"id": "any", "relation": "*", "color": "database-stroke", "label": "{relation_type}"}],
}
PAIR = {"light": "#fff1c2", "dark": "#3d3200"}


def _write(tmp_path, notation, name="infra.yml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(notation), encoding="utf-8")
    return path


def _store(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    return tmp_path / ".sldb"


def test_new_builtin_shapes_are_accepted(tmp_path):
    """spec2viz tests/test_style_palette.py::test_new_builtin_shapes_are_accepted."""
    assert {"cylinder", "queue", "cloud", "package", "note"} <= set(SHAPES)
    notation = copy.deepcopy(STYLED)
    notation["glyphs"] = [{"id": s, "model": "SpecNodeDoc", "where": f'kind = "{s}"', "shape": s} for s in ("cylinder", "queue", "cloud", "package", "note")]
    notation["glyphs"].append({"id": "any", "model": "SpecNodeDoc", "shape": "box"})
    load_notation(_write(tmp_path, notation))


def test_builtin_notations_still_validate_and_are_unstyled():
    """spec2viz tests/test_style_palette.py::test_builtin_notations_still_validate_and_are_unstyled."""
    for name in builtin_notations():
        assert load_notation(name).styled is False


def test_default_palette_is_accessible_and_distinguishable_without_colour():
    """spec2viz tests/test_style_palette.py::test_default_palette_is_accessible_and_distinguishable_without_colour."""
    palette = load_palette()
    assert set(palette.kinds) == {"database", "queue", "storage", "gateway", "auth", "backend", "frontend", "client", "external"}
    pairs = {(k.shape, k.icon) for k in palette.kinds.values()}
    assert len(pairs) == len(palette.kinds)  # forma + icono distinguen sin el tono
    for kind in palette.kinds.values():
        for theme in ("light", "dark"):
            assert contrast(palette.color(kind.stroke)[theme], getattr(palette.backgrounds, theme)) >= 3.0
            assert contrast(getattr(palette.ink, theme), palette.color(kind.fill)[theme]) >= 4.5


def test_precedence_glyph_over_spec_over_palette():
    """spec2viz tests/test_style_palette.py::test_precedence_glyph_over_spec_over_palette."""
    palette = {"colors": {k: v.model_dump() for k, v in load_palette().colors.items()},
               "kinds": {k: v.model_dump() for k, v in load_palette().kinds.items()}}
    # solo paleta
    style = resolve_style({}, "database", None, palette)
    assert style["fill"]["light"] == "#dbebf4" and style["icon"] == "database" and set(style["source"].values()) == {"palette"}
    # el spec gana a la paleta, propiedad por propiedad
    style = resolve_style({}, "database", {"database": {"fill": "#ffeecc"}}, palette)
    assert style["fill"] == {"light": "#ffeecc", "dark": "#ffeecc"} and style["source"]["fill"] == "spec" and style["source"]["stroke"] == "palette"
    # el glifo gana a todo: explicito, y detras el kind de la paleta que nombra
    style = resolve_style({"fill": "#000000", "kind": "queue"}, "database", {"database": {"fill": "#ffeecc", "icon": "cpu"}}, palette)
    assert style["fill"]["light"] == "#000000" and style["stroke"]["light"] == "#b37c00" and style["icon"] == "list-ordered"
    assert style["source"] == {"fill": "glyph", "stroke": "glyph", "icon": "glyph"}
    # sin paleta en la notacion, la paleta no aplica; el spec si (sus tokens resuelven contra default)
    assert resolve_style({}, "database", None, None) == {}
    assert resolve_style({}, "backend", {"backend": {"stroke": "backend-stroke"}}, None)["stroke"]["dark"] == "#56b4e9"


def test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched():
    """spec2viz tests/test_style_palette.py::test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched.

    Against specIR's renderers (`specir.visual.renderers`), which color with sldb's precedence."""
    diagram = load(FIXTURES / "component.kinds.yml")
    validate(diagram)
    out = MermaidRenderer().render(compile_ir(diagram))
    assert "classDef kind0 fill:#ffeecc,color:#1f2328" in out and "class db kind0" in out
    assert "classDef kind1 stroke:#1b8dce,color:#1f2328" in out and "class api kind1" in out
    assert "web" not in [l.split()[1] for l in out.splitlines() if l.strip().startswith("class ")]
    assert "classDef" not in MermaidRenderer().render(compile_ir(load(FIXTURES / "component.styled.yml")))
    assert "#112233" in PlantUMLRenderer().render(compile_ir(load(FIXTURES / "component.styled.yml")))


@pytest.mark.parametrize("entry, error", [({"fill": "blue"}, InvalidColorError), ({"icon": "rocket"}, UnknownIconError)])
def test_spec_style_kinds_are_validated_typed(entry, error):
    """spec2viz tests/test_style_palette.py::test_spec_style_kinds_are_validated_typed."""
    diagram = load(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = entry
    with pytest.raises(error):
        validate(diagram)


def test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend(tmp_path):
    """spec2viz tests/test_style_palette.py::test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend."""
    store = _store(tmp_path)
    notation = _write(tmp_path / "docs", STYLED)
    spec = shutil.copy(FIXTURES / "component.kinds.yml", tmp_path / "docs" / "kinds.yml")
    report = SpecSync(store).sync(Path(spec), notation=notation)
    assert "PaletteDoc:default" in report.created
    docs = {f"{d.model_name}:{d.name}": d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False)}
    assert docs["NotationDoc:infra"]["palette"] == "PaletteDoc:default"
    assert docs["GlyphDoc:infra.db"]["kind"] == "database" and docs["LinkDoc:infra.any"]["color"] == "database-stroke"
    assert docs["SpecDoc:component.kinds"]["style"] == {"database": {"fill": "#ffeecc"}, "backend": {"stroke": "backend-stroke", "icon": "cpu"}}

    view = resolve_view(store, "component.kinds")
    nodes = {n["element"]: n for n in view["nodes"]}
    # db: glifo con kind database (gana al spec), api: fill del glifo, stroke e icono del spec
    assert nodes["db"]["style"]["fill"]["light"] == "#dbebf4" and nodes["db"]["style"]["source"]["fill"] == "glyph"
    assert nodes["api"]["style"]["fill"]["light"] == "#fafafa" and nodes["api"]["style"]["icon"] == "cpu"
    assert nodes["api"]["style"]["source"] == {"fill": "glyph", "stroke": "spec", "icon": "spec"}
    # web: solo la paleta de la notacion
    assert nodes["web"]["style"]["icon"] == "app-window" and set(nodes["web"]["style"]["source"].values()) == {"palette"}
    assert all(l["color"] == {"light": "#0072b2", "dark": "#0072b2"} for l in view["links"])
    assert view["palette"] == "PaletteDoc:default"
    legend = view["legend"]
    assert [g["glyph"] for g in legend["glyphs"]] == ["GlyphDoc:infra.db", "GlyphDoc:infra.api", "GlyphDoc:infra.any"]
    assert legend["glyphs"][0]["shape"] == "cylinder" and legend["glyphs"][0]["style"]["icon"] == "database"
    assert legend["links"][0]["color"]["light"] == "#0072b2"
    assert {k["kind"] for k in legend["kinds"]} == {"backend", "frontend"} and next(k for k in legend["kinds"] if k["kind"] == "frontend")["shape"] == "box"


def test_unstyled_notation_writes_no_palette_and_no_style(tmp_path):
    """spec2viz tests/test_style_palette.py::test_unstyled_notation_writes_no_palette_and_no_style."""
    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "deployment.runtime.yml", tmp_path / "docs" / "dep.yml")
    SpecSync(store).sync(Path(spec))
    assert not any(str(d.model_name) == "PaletteDoc" for d in sldb_api.load_runtime_documents(store, None, include_linked=False))
    text = (tmp_path / "sldb" / "notations" / "deployment" / "notation.md").read_text(encoding="utf-8")
    assert "palette:" not in text
    view = resolve_view(store, "deployment.runtime")
    assert all(n["style"] == {} for n in view["nodes"]) and all(l["color"] is None for l in view["links"])


def test_resolve_documents_is_public_and_filters_relations(tmp_path):
    """spec2viz tests/test_style_palette.py::test_resolve_documents_is_public_and_filters_relations."""
    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "component.kinds.yml", tmp_path / "docs" / "kinds.yml")
    SpecSync(store).sync(Path(spec), notation=_write(tmp_path / "docs", STYLED))
    full = resolve_view(store, "component.kinds")
    refs = [n["doc"] for n in full["nodes"]]
    same = resolve_documents(store, "NotationDoc:infra", refs, spec_style={"database": {"fill": "#ffeecc"}, "backend": {"stroke": "backend-stroke", "icon": "cpu"}})
    assert [n["style"] for n in same["nodes"]] == [n["style"] for n in full["nodes"]] and same["links"] == full["links"]
    # api y db, y solo la arista api -> db aunque web -> api tambien exista
    keep = {r for r in refs if r.endswith((".api", ".db"))}
    edge = next(l["doc"] for l in full["links"] if l["source"] in keep and l["target"] in keep)
    one = resolve_documents(store, "infra", sorted(keep), relation_refs=[edge])
    assert len(one["nodes"]) == 2 and [l["doc"] for l in one["links"]] == [edge]
    assert resolve_documents(store, "infra", sorted(keep), relation_refs=[])["links"] == []


@pytest.mark.parametrize("value, error", [
    ({"light": "#fff1c2"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "#3d3200", "hc": "#000000"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "dark-yellow"}, "dark"),
    ({"light": "fff1c2", "dark": "#3d3200"}, "light"),
])
def test_color_pair_is_validated_typed(tmp_path, value, error):
    """spec2viz tests/test_style_palette.py::test_color_pair_is_validated_typed."""
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = value
    with pytest.raises(InvalidColorError, match=error):
        load_notation(_write(tmp_path, notation))


def test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not():
    """spec2viz tests/test_style_palette.py::test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not."""
    assert resolve_color("#FFF1C2", {}) == {"light": "#fff1c2", "dark": "#fff1c2"}
    tokens = {k: v.model_dump() for k, v in load_palette().colors.items()}
    assert resolve_color(PAIR, tokens) == PAIR
    # cada lado puede ser un token: se toma el valor de ese tema
    assert resolve_color({"light": "#fff1c2", "dark": "queue-fill"}, tokens) == {"light": "#fff1c2", "dark": "#4a3911"}


def test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec(tmp_path):
    """spec2viz tests/test_style_palette.py::test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec."""
    store = _store(tmp_path)
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = PAIR
    notation["glyphs"][1]["stroke"] = {"light": "#7a5c00", "dark": "#e6c34a"}
    notation["links"][0]["color"] = {"light": "#0072b2", "dark": "#56b4e9"}
    spec = yaml.safe_load((FIXTURES / "component.kinds.yml").read_text(encoding="utf-8"))
    spec["style"]["kinds"]["frontend"] = {"fill": {"light": "#eef6ff", "dark": "#10233a"}}
    (tmp_path / "docs" / "kinds.yml").write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")
    SpecSync(store).sync(tmp_path / "docs" / "kinds.yml", notation=_write(tmp_path / "docs", notation))

    glyph = next(d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if d.name == "infra.api")
    assert glyph["fill"] == PAIR  # el GlyphDoc guarda el par tal cual
    nodes = {n["element"]: n for n in resolve_view(store, "component.kinds")["nodes"]}
    assert nodes["api"]["style"]["fill"] == PAIR and nodes["api"]["style"]["stroke"] == {"light": "#7a5c00", "dark": "#e6c34a"}
    assert nodes["web"]["style"]["fill"] == {"light": "#eef6ff", "dark": "#10233a"} and nodes["web"]["style"]["source"]["fill"] == "spec"
    view = resolve_view(store, "component.kinds")
    assert {l["color"]["dark"] for l in view["links"]} == {"#56b4e9"}


def test_mermaid_takes_the_light_side_of_a_spec_pair():
    """spec2viz tests/test_style_palette.py::test_mermaid_takes_the_light_side_of_a_spec_pair.

    Against specIR's mermaid renderer (`specir.visual.renderers.mermaid`)."""
    diagram = load(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = {"fill": PAIR}
    validate(diagram)
    assert "classDef kind0 fill:#fff1c2,color:#1f2328" in MermaidRenderer().render(compile_ir(diagram))

FILE:src/specir/visual/notation_style.py
"""Style resolution and the error root of sldb's notations, taken from SLDB, never defined here.

The renderers color elements with the one precedence that sldb owns (glyph > `style.kinds` of the
spec > palette, `sldb.notations.resolve_style`) and write text in the ink of sldb's builtin
`default` palette (`sldb.notations.load_palette`). The commands report sldb's loading and
validation errors (`sldb.notations.NotationError`, the root of `ParseError` and `ValidationError`).
The catalog (IR13b) reports the typed errors of the catalog path rule (`AmbiguousPathError`,
`UnknownReferenceError`, `UnknownNotationError`) and picks a view's notation with
`DEFAULT_NOTATIONS` and `builtin_notations`.
The notation and palette tests ported from spec2viz (IR13e, tests/visual/test_notations_parity.py)
load, validate and compare sldb's notations and palettes with the rest of what this module
re-exports from `sldb.notations`: `load_notation`, `NotationSpec`, `SHAPES`, `DiagramType`,
`load_palette`, `PaletteSpec`, `check_palette`, `contrast`, `resolve_color` and the typed errors
(`ValidationError`, `InvalidColorError`, `UnknownIconError`, `UnknownKindError`,
`UnknownShapeError`). Nothing here is defined by specIR.
`sldb.api` does not export these yet (asked to sldb's desk), so this module is the only one of
specIR that reaches `sldb.notations` (tests/test_imports.py allows it here and nowhere else). When
sldb exports them from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from functools import lru_cache

from sldb.notations import (
    DEFAULT_NOTATIONS,
    SHAPES,
    AmbiguousPathError,
    DiagramType,
    InvalidColorError,
    NotationError,
    NotationSpec,
    PaletteSpec,
    UnknownIconError,
    UnknownKindError,
    UnknownNotationError,
    UnknownReferenceError,
    UnknownShapeError,
    ValidationError,
    builtin_notations,
    check_palette,
    contrast,
    load_notation,
    load_palette,
    resolve_color,
    resolve_style,
)


@lru_cache(maxsize=1)
def default_ink() -> dict[str, str]:
    """The text color (`{light, dark}`) of sldb's builtin `default` palette."""
    return load_palette().ink.model_dump()


__all__ = [
    "DEFAULT_NOTATIONS", "SHAPES", "AmbiguousPathError", "DiagramType", "InvalidColorError", "NotationError",
    "NotationSpec", "PaletteSpec", "UnknownIconError", "UnknownKindError", "UnknownNotationError",
    "UnknownReferenceError", "UnknownShapeError", "ValidationError", "builtin_notations", "check_palette",
    "contrast", "default_ink", "load_notation", "load_palette", "resolve_color", "resolve_style",
]

FILE:docs/spec2viz/acta-de-retiro.md
# Acta de retiro de spec2viz

Tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`). Evaluación del
2026-11-15 sobre IR `dc5496a`, sldb `d4aeb4b1` y el inventario de consumidores de
`docs/spec2viz/matriz-de-cobertura.md`.

**Retiro: no declarado.** El comprobador `specir retirement check` sale con código 1: quedan 119
dependencias de spec2viz en el universo auditado y 13 filas de la matriz sin acreditar (re-corrida del
2026-11-16 tras IR13e, que portó contra sldb las pruebas de notaciones, paletas y vistas; antes eran 23,
y 30 antes de las decisiones de JP y la corrida con mermaid-cli real). Archivar o borrar
spec2viz lo decide JP cuando el gate se cumpla; esta tarea no lo hace.

## Comprobador

`specir retirement check` (`src/specir/visual/retirement.py`, pruebas en
`tests/visual/test_retirement_gate.py`) audita en solo lectura exactamente los repos y stores del
inventario de la matriz más el repo de specIR, y la sección «Acreditación (IR13)» de la matriz. Cada
dependencia sale con repo o store, ruta, línea y clase (importación, dependencia declarada, invocación del
comando, habilidad de agente, modelo registrado). Un nombre fuera del inventario o uno del inventario sin
ruta es un error de uso (código 2). Las menciones en prosa, documentación, comentarios, docstrings,
changelogs y documentos del desk no cuentan.

Corrida real:

```
cd IR && .venv/bin/specir retirement check \
  --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron \
  --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb
```

rc 1; 119 dependencias; 13 filas no acreditadas (SV-A17, G08, H01, H03, I02, K09, K16, K18, K21, K22,
K23, K26 y K29). Corrida del 2026-11-16 tras IR13e
(`task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`), sobre
sldb `9307d485` y spec2viz `91ba1d0` (b624b75 más un commit solo de desk/store): antes de IR13e eran 23
filas (SV-A17, E02, G08, H01 a H06, I02, J06, K09, K16, K18 a K26 y K29) y 119 dependencias; las 122 de
la corrida del 2026-11-15 bajaron a 119 porque ya no aparecen las 3 invocaciones de pron
(`docs/spec2viz/build.py:22` a `:24`), cambio ajeno a IR13e. La prueba
`test_the_real_universe_has_no_dependency_and_every_row_is_accredited` es un xfail estricto mientras esto
siga así: cuando pase, la suite lo marca y hay que quitar el xfail y declarar el retiro aquí.

## Gate G1 a G7

| Ítem | Estado | Evidencia |
|---|---|---|
| G1 Filas cumplidas | abierto | 92 cumplidas y 13 abiertas en «Acreditación (IR13)» de la matriz. IR13e (2026-11-16) acreditó SV-E02, SV-H02, SV-H04, SV-H05, SV-H06, SV-J06, SV-K19, SV-K20, SV-K24 y SV-K25; la corrida con mermaid-cli real del 2026-11-15 acreditó SV-B03, SV-C13, SV-C14, SV-D01, SV-G03, SV-K12 y SV-K17. |
| G2 Suite de spec2viz | abierto | Portadas contra sldb por IR13e en `tests/visual/test_notations_parity.py` (75 passed, 1 xfailed): las 40 pruebas no CLI de `tests/test_view_doc.py`, `test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py` y `test_style_palette.py`, más 9 comparaciones «valida igual»; las 6 que invocan el CLI de spec2viz tienen su equivalente en las filas K. xfail estricto: el mensaje de `diagram_type` desconocido de test_invalid_notations_are_rejected (SV-H01, nota a sldb 20261116-022332). Los casos de mmdc (`test_mermaid_mmdc.py` y los de motor real de `test_class_diagram.py`, `test_class_packages.py` y `test_catalog_resolved_views.py`) ya corren con mermaid-cli real y pasan (2026-11-15). xfail estricto: `label_key` frente a `normKey` (`test_atoms_matching.py`). Los 38 archivos tienen fila (`tests/test_matriz_cobertura_spec2viz.py`, 5 passed). |
| G3 CLI | abierto | Los 30 equivalentes existen y los invoca `test_every_equivalent_of_the_table_answers_its_help` (`tests/visual/test_cli.py`, 44 passed). Faltan los comandos de sldb para validar notación y paleta (SV-K21, SV-K26) y el de validar un spec, que hoy da specIR de forma provisional (SV-K16, SV-K29). Nota de sldb `20261115-192054`. |
| G4 Consumidores | abierto | 119 dependencias (abajo; corrida del 2026-11-16). |
| G5 Stores | abierto | `spec2viz/.sldb` registra los 7 modelos de `spec2viz.sldb_models` (19 registros). Es el único store del universo que lo hace. |
| G6 specIR limpio | cumplido | `tests/test_imports.py` (9 passed): nada bajo `src/specir/` importa spec2viz; `test_specir_defines_no_command_the_table_gives_to_sldb`. |
| G7 Decisión del YAML | cumplido | JP aceptó el 2026-11-15 (vía supervisor) que el YAML del spec queda como formato de autoría e intercambio subordinado al grafo: `docs/decisiones/fuente-de-verdad-del-diagrama.md` y atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al` (la propuesta de IR07 quedó como redirección). |

## Consumidores

| Consumidor | Dependencias (clase) | Mensaje enviado | Cambio que lo resolvió |
|---|---|---|---|
| graph_ui | 34: 9 importaciones (`frontends/mindmap/sldb_adapter.py:245`, `:437` y pruebas), 3 declaradas (`pyproject.toml:19`, `:24`, `.github/requirements-suite.txt:10`), 22 invocaciones en pruebas | `UIs/graph_ui/desk/inbox/20261115-224814-suggestion-ir13-pide-migrar-graph-ui-de-spec2viz-a-sldb-resolve-view-sync-de-specs-viewdoc-pilotos.md` | pendiente |
| deskops | 22: 20 de habilidad de agente (`.claude/skills/deskops-workflow/SKILL.md`, `references/spec2viz-cli.md`, `.opencode/skills/use-spec2viz/SKILL.md`), 2 invocaciones (`desk/drawer/plans/workspace-documental/render_diagram.py:7`, `:9`). Además, la regla de rutas `deskops/graph/desk_graph.py:75` (no es dependencia; decidida, ver «Decisiones» 4) | `deskops/desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md` | pendiente |
| pron | 3 invocaciones (`docs/spec2viz/build.py:22`, `:23`, `:24`) | `pron/desk/inbox/20261115-224816-suggestion-ir13-pide-pasar-docs-spec2viz-build-py-de-pron-de-spec2viz-a-specir.md` | pendiente |
| sldb | 1 importación (oráculo de D2, `tests/notations/test_component_spec_python.py:43`). Además, el registro `docs/architecture/spec2viz/vistas.yml` que se construye con `spec2viz catalog build` y `contracts/identity.toml:299` (no son dependencias para el comprobador) | `sldb/desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md` | pendiente |
| store `spec2viz/.sldb` | 19 modelos registrados | `spec2viz/desk/inbox/20261115-225013-suggestion-ir13-el-store-de-spec2viz-es-el-nico-que-registra-spec2viz-sldb-models-gate-g5.md` | pendiente |
| IR (specIR) | 43 importaciones, todas en pruebas: los oráculos de paridad (`tests/visual/parity.py`, `render_parity.py` y los `importorskip("spec2viz")` de las pruebas de paridad) y la lectura del CLI de spec2viz en `tests/test_matriz_cobertura_spec2viz.py:31`. Se saltan sin spec2viz. Además, `tests/conftest.py:24` y `:80` y `tests/test_mcp_extension.py:24` federan el store `spec2viz/.sldb` (no es dependencia para el comprobador, pero la suite falla si el store desaparece) | propio: se resuelve en IR al declarar el retiro (quitar oráculos que ya tienen goldens, guardar como golden la corrida de paridad del catálogo de IR13b y cambiar la federación por un fixture) | pendiente |

Para enviar los mensajes se registraron en `desk/registry` de IR los repos deskops, pron, graph_ui (id
`graph-ui`) y spec2viz con `deskops repo register`; antes solo estaba sldb.

## Salida del comprobador (dependencias)

```
graph_ui	.github/requirements-suite.txt:10	dependencia declarada	-e git+https://github.com/jpcosec/spec2viz@master#egg=spec2viz
graph_ui	frontends/mindmap/sldb_adapter.py:245	importación	from spec2viz.notation_view import ViewError, resolve_view
graph_ui	frontends/mindmap/sldb_adapter.py:437	importación	from spec2viz.notation_view import ViewError, resolve_documents
graph_ui	pyproject.toml:19	dependencia declarada	notation = ["spec2viz>=0.1.0"]
graph_ui	pyproject.toml:24	dependencia declarada	"spec2viz>=0.1.0",
graph_ui	tests/e2e_mindmap_notation.py:27	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/e2e_mindmap_notation.py:42	invocación del comando	if not all(p.exists() for p in pilots) or not shutil.which("spec2viz"):
graph_ui	tests/e2e_mindmap_notation.py:48	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *(p.name for p in pilots), "--store", ".sldb"],
graph_ui	tests/e2e_notation_activity.py:121	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_activity.py:128	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_class.py:51	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_class.py:58	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_deployment.py:85	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_deployment.py:92	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_legibility.py:38	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/e2e_notation_legibility.py:169	invocación del comando	if not ACTIVITY.exists() or not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_legibility.py:175	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", FIXTURE.name, DENSE.name, ACTIVITY.name, "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_sequence.py:101	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_sequence.py:108	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_style.py:141	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_style.py:147	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", "component-infra.yml", "--notation", "infra.yml", "--store", ".sldb"],
graph_ui	tests/e2e_review_workbench_views.py:40	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/e2e_review_workbench_views.py:76	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *pilots, "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_review_workbench_views.py:86	invocación del comando	if not all((PILOTS / p).exists() for p in HERE + THERE) or not shutil.which("spec2viz"):
graph_ui	tests/e2e_review_workbench_views.py:96	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", "component-infra.yml", "--notation", "infra.yml", "--store", ".sldb"],
graph_ui	tests/test_mindmap_notation.py:20	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/test_mindmap_notation.py:21	importación	from spec2viz.notation_view import resolve_view  # noqa: E402
graph_ui	tests/test_mindmap_notation.py:40	invocación del comando	if not all(p.exists() for p in pilots) or not shutil.which("spec2viz"):
graph_ui	tests/test_mindmap_notation.py:45	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *(p.name for p in pilots), "--store", ".sldb"],
graph_ui	tests/test_projection_views.py:18	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/test_projection_views.py:28	invocación del comando	if not all((PILOTS / p).exists() for p in pilots) or not shutil.which("spec2viz"):
graph_ui	tests/test_projection_views.py:33	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *pilots, "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/test_projection_views.py:82	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", "component-infra.yml", "--notation", "infra.yml", "--store", ".sldb"],
graph_ui	tests/test_projection_views.py:167	importación	pytest.importorskip("spec2viz.sldb_models").ViewDoc  # task a: the model lives in spec2viz
deskops	.claude/skills/deskops-workflow/SKILL.md:27	habilidad de agente	(`spec2viz diagram render` / `spec2viz catalog build`) derive from specs and decisions. Atoms
deskops	.claude/skills/deskops-workflow/SKILL.md:59	habilidad de agente	re-run `spec2viz diagram render` / `spec2viz catalog build`. Validate before rendering:
deskops	.claude/skills/deskops-workflow/SKILL.md:60	habilidad de agente	`spec2viz diagram validate <spec.yml>`.
deskops	.claude/skills/deskops-workflow/SKILL.md:101	habilidad de agente	| Validate a diagram spec | `spec2viz diagram validate <spec.yml>` |
deskops	.claude/skills/deskops-workflow/SKILL.md:102	habilidad de agente	| Render a diagram | `spec2viz diagram render <spec.yml> --out <dir> [--renderer mermaid\|plantuml\|vega\|d2\|antonia-html\|json]` |
deskops	.claude/skills/deskops-workflow/SKILL.md:103	habilidad de agente	| Build a diagram catalog | `spec2viz catalog build --config <catalog.yml> --out <out.html>` |
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:8	habilidad de agente	commands (`spec2viz render`, `spec2viz validate`, `spec2viz schema`, `spec2viz lint`) remain as
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:13	habilidad de agente	- `spec2viz diagram validate <spec.yml> [<spec2.yml> ...]` — validate one or more diagram specs
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:15	habilidad de agente	- `spec2viz diagram render <spec.yml> [<spec2.yml> ...] --out <dir> \
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:19	habilidad de agente	- `spec2viz diagram schema [--type sequence|state|component|activity|deployment|matrix] [--out <file>]`
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:21	habilidad de agente	- `spec2viz diagram generate` — generate a component spec from Python source AST (reverse
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:23	habilidad de agente	- `spec2viz diagram lint <spec-or-mmd> [...]` — lint rendered Mermaid for browser-breaking syntax.
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:27	habilidad de agente	- `spec2viz catalog build --config <vistas.yml-or-diagram-store.yml> --out <out.html> \
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:33	habilidad de agente	- `spec2viz catalog schema [--out <file>]` — JSON Schema for diagram-store / `project.yml` configs.
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:34	habilidad de agente	- `spec2viz catalog serve` — serve a built catalog locally with auto-save for viewer annotations
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:80	habilidad de agente	- `spec2viz render <spec.yml> --out <dir> [--renderer ...]` == `spec2viz diagram render`
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:81	habilidad de agente	- `spec2viz validate <spec.yml>` == `spec2viz diagram validate`
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:82	habilidad de agente	- `spec2viz schema [--type ...] [--out ...]` == `spec2viz diagram schema` (also accepts
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:84	habilidad de agente	- `spec2viz lint <spec-or-mmd>` == `spec2viz diagram lint`
deskops	.opencode/skills/use-spec2viz/SKILL.md:2	habilidad de agente	name: use-spec2viz
deskops	desk/drawer/plans/workspace-documental/render_diagram.py:7	invocación del comando	subprocess.run(['spec2viz','diagram','validate',str(B/'dag.diagram.yaml')],check=True)
deskops	desk/drawer/plans/workspace-documental/render_diagram.py:9	invocación del comando	subprocess.run(['spec2viz','diagram','render',str(B/'dag.diagram.yaml'),'--renderer',renderer,'--out',str(B)],check=True)
sldb	tests/notations/test_component_spec_python.py:43	importación	python_ast = pytest.importorskip("spec2viz.generators.python_ast")
IR	tests/test_matriz_cobertura_spec2viz.py:31	importación	main = importlib.import_module("spec2viz.cli").main
IR	tests/visual/parity.py:52	importación	from spec2viz.compilers import compile_ir
IR	tests/visual/parity.py:53	importación	from spec2viz.loader import load
IR	tests/visual/parity.py:54	importación	from spec2viz.validator import validate
IR	tests/visual/render_parity.py:74	importación	from spec2viz.compilers import compile_ir
IR	tests/visual/render_parity.py:75	importación	from spec2viz.loader import load
IR	tests/visual/render_parity.py:76	importación	from spec2viz.renderers import render
IR	tests/visual/render_parity.py:77	importación	from spec2viz.renderers.bpmn import render_bpmn_html
IR	tests/visual/render_parity.py:87	importación	from spec2viz.cli import DIAGRAM_RENDERERS
IR	tests/visual/render_parity.py:88	importación	from spec2viz.renderers import DEFAULT_RENDERER, EXT_MAP
IR	tests/visual/render_parity.py:94	importación	from spec2viz.renderers.view_mermaid import view_to_mermaid
IR	tests/visual/render_parity.py:100	importación	from spec2viz.linters.mermaid import lint_mermaid
IR	tests/visual/render_parity.py:106	importación	from spec2viz.schema import json_schema
IR	tests/visual/render_parity.py:112	importación	from spec2viz import render_to_file
IR	tests/visual/render_parity.py:119	importación	import spec2viz
IR	tests/visual/render_parity.py:190	importación	from spec2viz.linters.mermaid import lint_mermaid
IR	tests/visual/render_parity.py:191	importación	from spec2viz.schema import json_schema
IR	tests/visual/test_catalog_parity.py:39	importación	spec2viz = pytest.importorskip("spec2viz")
IR	tests/visual/test_catalog_parity.py:49	importación	from spec2viz.sldb_sync import check_catalog as oracle
IR	tests/visual/test_catalog_parity.py:102	importación	from spec2viz.sldb_sync import SpecSync as OracleSync
IR	tests/visual/test_catalog_parity.py:103	importación	from spec2viz.sldb_sync import sync_catalog as oracle_sync
IR	tests/visual/test_catalog_parity.py:122	importación	from spec2viz.cli import main
IR	tests/visual/test_catalog_parity.py:154	importación	from spec2viz.deskops import render_deskops
IR	tests/visual/test_catalog_parity.py:203	importación	from spec2viz.deskops import render_deskops
IR	tests/visual/test_lint_mermaid.py:86	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_cases.py:314	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_commands.py:251	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:53	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:59	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:83	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_resources.py:62	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_schema.py:44	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:105	importación	spec2viz = pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:117	importación	from spec2viz.sldb_sync import SpecSync as Spec2VizSync
IR	tests/visual/test_sync_generation_parity.py:201	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:229	importación	import spec2viz.graph_import as oracle
IR	tests/visual/test_sync_generation_parity.py:258	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:259	importación	from spec2viz.graph_import import component_spec_from_graph as oracle_from_graph
IR	tests/visual/test_sync_generation_parity.py:260	importación	from spec2viz.graph_import import load_store_index
IR	tests/visual/test_sync_generation_parity.py:302	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:303	importación	from spec2viz.generators.python_ast import generate_python_ast_spec
IR	tests/visual/test_visual_parity.py:35	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_visual_parity.py:43	importación	pytest.importorskip("spec2viz")
spec2viz/.sldb	store.yaml:44	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	store.yaml:47	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	store.yaml:50	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	store.yaml:53	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	store.yaml:56	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/store_index.yaml:141	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	core/store_index.yaml:154	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	core/store_index.yaml:167	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	core/store_index.yaml:180	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	core/store_index.yaml:193	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/store_index.yaml:246	modelo registrado	model_ref: spec2viz.sldb_models:ViewDoc
spec2viz/.sldb	core/store_index.yaml:259	modelo registrado	model_ref: spec2viz.sldb_models:PaletteDoc
spec2viz/.sldb	core/models/GlyphDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	core/models/LinkDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/models/NotationDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	core/models/PaletteDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:PaletteDoc
spec2viz/.sldb	core/models/SpecDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	core/models/SpecNodeDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	core/models/ViewDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:ViewDoc
```

## Medición de `specir catalog build` (pendiente de IR13d)

`specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml` dentro de IR
no termina en 300 s (`timeout 300`, rc 124, 3 min 50 s de CPU). Con cProfile (corrida cortada a los
150 s), 146 de los 149 s se van en `sldb.api.matching.attach_atom_edges`. Esa función hace 31 llamadas a
`StoreReader.edges_of`, que suman 62 llamadas a `load_edge_index` de ~1,1 s cada una:

- `with_live_stale` recalcula el stale vivo en cada llamada (284 251 `_moved`, 63 s).
- `EdgeIndex._ensure_maps` reconstruye los mapas en cada copia (61 veces, 66 s).

El store que descubre el catálogo es el `.sldb` de IR, que federa 8 stores (con `deskops` y `sldb`
duplicados desde `/mnt/ssd/herramientas`). Ahí `load_edge_index` tarda 28,6 s la primera vez y 0,4 s las
siguientes, pero devuelve un objeto nuevo cada vez (1963 stale).

Es de sldb, no de specIR: specIR solo usa la API pública. Pedido en
`sldb/desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md`.

## Lo que falta para declarar el retiro

1. Consumidores (G4): que graph_ui, deskops, pron y sldb resuelvan sus pedidos y respondan con el commit.
2. Store (G5): reapuntar los modelos de `spec2viz/.sldb` a los de sldb, o archivar el store con el repo
   (decisión del dueño).
3. Filas «usar sldb directamente»: portadas por IR13e (`tests/visual/test_notations_parity.py`). Quedan
   SV-H01 (sldb da otro mensaje ante un `diagram_type` desconocido; nota a sldb 20261116-022332), SV-A17
   (solo G5), SV-H03 y su dependiente SV-K22 (solo G4 de graph_ui), y SV-K18 y SV-K23 (dependen de SV-K21,
   SV-K22 y SV-K26).
4. sldb: comando para validar spec, notación y paleta (SV-K16, K21, K26, K29; después hay que retirar
   `specir diagram validate`/`validate`). También el `label_key` con `_` (SV-G08 y SV-I02).
5. mmdc: resuelto el 2026-11-15. Con mermaid-cli real (`SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc`)
   pasan los casos de motor real; quedaron cumplidas SV-B03, C13, C14, D01, G03, K12 y K17. SV-K09 sigue
   abierta por SV-K16.
6. IR: quitar o congelar los oráculos de paridad y la federación del store de spec2viz en las pruebas.
7. G7: resuelto el 2026-11-15 (decisión aceptada por JP; ver «Decisiones»).
8. En el momento del retiro: el BPMN pasa a `exporter="specir"` y a un `targetNamespace` de specir, y la
   página del catálogo a una clave de `localStorage` de specir, con goldens nuevos y migración de las
   anotaciones guardadas con `spec2viz.catalog.annotations.v1` (decisión 3).
9. Archivar spec2viz cuando `specir retirement check` salga con 0 (decisión 6).

## Decisiones

Registradas el 2026-11-15. Todas aceptadas por JP (transmitidas por el supervisor con autorización
explícita).

1. **G7, el YAML del spec** (decisión del dueño, JP): el YAML del spec queda como formato de autoría e
   intercambio subordinado al grafo, según `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Registro:
   atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`
   (la propuesta `atom-propuesta-pendiente-de-jp-…` se fusionó en él con `deskops atoms merge`). No hay
   task.decision asociada a G7 en el desk de IR.
2. **mmdc con motor real**: JP autorizó lanzar `/usr/bin/google-chrome` para mermaid-cli. Instalado en
   `/mnt/ssd/herramientas/mermaid-cli` (fuera de los repos), con un envoltorio `mmdc` que corre Chrome en
   headless con `timeout` y perfil temporal en `/dev/shm`. Cómo apuntar `SPECIR_MMDC`: habilidad
   `skills/use-specir/SKILL.md`, sección «Real mermaid engine (mmdc)».
3. **Exporter de BPMN y clave de `localStorage`** (elegida por el coordinador): mientras dure la paridad se
   mantienen `exporter="spec2viz"`, `targetNamespace="http://spec2viz/bpmn"` (SV-C06) y la clave
   `spec2viz.catalog.annotations.v1` (SV-G06). En el momento del retiro pasan a specir con goldens nuevos
   y migración de anotaciones (paso 8 de la lista anterior).
4. **deskops, regla de rutas** (elegida por el coordinador; la ejecuta el desk de deskops, no IR):
   `deskops/graph/desk_graph.py:75` deja de nombrar spec2viz y reconoce los specs YAML como artefactos de
   autoría sincronizados con `sldb notations sync`.
5. **sldb, `docs/architecture/spec2viz`** (elegida por el coordinador; la ejecuta el desk de sldb, no IR):
   los specs se quedan como fixtures durante la paridad; el catálogo se construye con
   `specir catalog build` y se sincroniza con `sldb notations sync --catalog`.
6. **Archivo de spec2viz**: spec2viz se archiva cuando `specir retirement check` salga con 0.

FILE:instruccion
Cold-bundle de la tarea task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_notations_parity.py sale con rc 0 y tiene las 42 pruebas portadas (40, más test_notation_load_gives_typed_errors y test_palette_check_is_typed, con sus 7 y 6 casos) más las 9 comparaciones «valida igual» (passed o xfailed estricto, ninguna skipped).
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider -rxX tests/visual/test_catalog.py sale con rc 0, sin xfailed ni xpassed para las pruebas de label_key (respaldo de SV-G08 y SV-I02).
- grep -rnE '^(from|import) spec2viz' tests/visual/test_notations_parity.py no encuentra nada, y grep -rnE 'from sldb\.(notations|models|store|core)' tests/visual/test_notations_parity.py tampoco.
- timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb lista como no acreditadas solo filas que siguen abiertas en la matriz con su motivo, y ninguna de las filas que la matriz da por cumplidas; su salida queda en docs/spec2viz/acta-de-retiro.md.
- Suite completa una vez, bajo flock /dev/shm/sldb1-tests.lock, con el comando SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.
- deskops graph missing --root . sale con rc 0.

