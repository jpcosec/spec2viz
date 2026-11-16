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

FILE:src/specir/visual/notation_style.py
"""Style resolution and the error root of sldb's notations, taken from SLDB, never defined here.

The renderers color elements with the one precedence that sldb owns (glyph > `style.kinds` of the
spec > palette, `sldb.notations.resolve_style`) and write text in the ink of sldb's builtin
`default` palette (`sldb.notations.load_palette`). The commands report sldb's loading and
validation errors (`sldb.notations.NotationError`, the root of `ParseError` and `ValidationError`).
The catalog (IR13b) reports the typed errors of the catalog path rule (`AmbiguousPathError`,
`UnknownReferenceError`, `UnknownNotationError`) and picks a view's notation with
`DEFAULT_NOTATIONS` and `builtin_notations`.
`sldb.api` does not export these yet (asked to sldb's desk), so this module is the only one of
specIR that reaches `sldb.notations` (tests/test_imports.py allows it here and nowhere else). When
sldb exports them from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from functools import lru_cache

from sldb.notations import (
    DEFAULT_NOTATIONS,
    AmbiguousPathError,
    NotationError,
    UnknownNotationError,
    UnknownReferenceError,
    builtin_notations,
    load_palette,
    resolve_style,
)


@lru_cache(maxsize=1)
def default_ink() -> dict[str, str]:
    """The text color (`{light, dark}`) of sldb's builtin `default` palette."""
    return load_palette().ink.model_dump()


__all__ = [
    "DEFAULT_NOTATIONS", "AmbiguousPathError", "NotationError", "UnknownNotationError", "UnknownReferenceError",
    "builtin_notations", "default_ink", "resolve_style",
]

FILE:docs/spec2viz/acta-de-retiro.md
# Acta de retiro de spec2viz

Tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`). Evaluación del
2026-11-15 sobre IR `dc5496a`, sldb `d4aeb4b1` y el inventario de consumidores de
`docs/spec2viz/matriz-de-cobertura.md`.

**Retiro: no declarado.** El comprobador `specir retirement check` sale con código 1: quedan 122
dependencias de spec2viz en el universo auditado y 23 filas de la matriz sin acreditar (re-corrida del
2026-11-15 tras las decisiones de JP y la corrida con mermaid-cli real; antes eran 30). Archivar o borrar
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

rc 1; 122 dependencias; 23 filas no acreditadas (SV-A17, E02, G08, H01 a H06, I02, J06, K09, K16, K18
a K26 y K29). La prueba
`test_the_real_universe_has_no_dependency_and_every_row_is_accredited` es un xfail estricto mientras esto
siga así: cuando pase, la suite lo marca y hay que quitar el xfail y declarar el retiro aquí.

## Gate G1 a G7

| Ítem | Estado | Evidencia |
|---|---|---|
| G1 Filas cumplidas | abierto | 82 cumplidas y 23 abiertas en «Acreditación (IR13)» de la matriz (la corrida con mermaid-cli real del 2026-11-15 acreditó SV-B03, SV-C13, SV-C14, SV-D01, SV-G03, SV-K12 y SV-K17). |
| G2 Suite de spec2viz | abierto | Sin portar: `tests/test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py`, `test_style_palette.py`, `test_view_doc.py` (filas «usar sldb directamente», eran de IR13c). Los casos de mmdc (`test_mermaid_mmdc.py` y los de motor real de `test_class_diagram.py`, `test_class_packages.py` y `test_catalog_resolved_views.py`) ya corren con mermaid-cli real y pasan (2026-11-15). xfail estricto: `label_key` frente a `normKey` (`test_atoms_matching.py`). Los 38 archivos tienen fila (`tests/test_matriz_cobertura_spec2viz.py`, 5 passed). |
| G3 CLI | abierto | Los 30 equivalentes existen y los invoca `test_every_equivalent_of_the_table_answers_its_help` (`tests/visual/test_cli.py`, 44 passed). Faltan los comandos de sldb para validar notación y paleta (SV-K21, SV-K26) y el de validar un spec, que hoy da specIR de forma provisional (SV-K16, SV-K29). Nota de sldb `20261115-192054`. |
| G4 Consumidores | abierto | 122 dependencias (abajo). |
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
pron	docs/spec2viz/build.py:22	invocación del comando	run('spec2viz', 'diagram', 'validate', *specs)
pron	docs/spec2viz/build.py:23	invocación del comando	run('spec2viz', 'diagram', 'render', *specs, '--backend', 'mermaid', '--out', 'out/mermaid')
pron	docs/spec2viz/build.py:24	invocación del comando	run('spec2viz', 'catalog', 'build', '--config', 'catalog.yml', '--out', 'index.html')
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
3. Filas «usar sldb directamente» (SV-A17, SV-E02, SV-H01 a SV-H06, SV-J06, SV-K18 a SV-K26): portar los
   casos de `tests/test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py`,
   `test_style_palette.py` y `test_view_doc.py` contra la API de sldb, sin envoltorio. Ninguna tarea lo
   tiene desde que se retiró IR13c.
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
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_notations_parity.py sale con rc 0 y reporta las 40 pruebas portadas más las 9 comparaciones «valida igual» (passed o xfailed estricto, ninguna skipped).
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_imports.py tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- grep -rnE '^(from|import) spec2viz' tests/visual/test_notations_parity.py no encuentra nada, y grep -rnE 'from sldb\.(notations|models|store|core)' tests/visual/test_notations_parity.py tampoco.
- timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb lista como no acreditadas solo filas que siguen abiertas en la matriz con su motivo, y ninguna de las filas que la matriz da por cumplidas; su salida queda en docs/spec2viz/acta-de-retiro.md.
- {'Suite completa una vez, bajo flock /dev/shm/sldb1-tests.lock': 'SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.'}
- deskops graph missing --root . sale con rc 0.

