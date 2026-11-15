FILE:desk/tasks/task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro.md
---
sldb:
  by: agent
  at: '2026-11-15T21:36:16Z'
  authority: generated
  via: save_document_payload
id: task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
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
- task-ir03-servidor-mcp-de-solo-lectura-sobre-un-store-sldb-real
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
pills:
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/gate-de-retiro.md
- docs/decisiones/fuente-de-verdad-del-diagrama.md
- tests/test_matriz_cobertura_spec2viz.py
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
- atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al
from_drawer: desk/drawer/tasks/task-ir07-matriz-de-cobertura-de-spec2viz-para-su-retiro.md
---

# IR07 Cobertura completa de spec2viz: matriz, fuente de verdad del diagrama y gate de retiro

## Rationale

_Explain why this task exists or the business driver behind it._

specIR debe cubrir todas las funcionalidades de spec2viz para poder retirarlo. Sin una lista completa con el modo de cobertura de cada cosa, el retiro no es verificable. Además conviven dos modelos de diagrama: en spec2viz el YAML del spec es la fuente y el store es derivado; en specIR la fuente semántica es el grafo de SLDB y el diagrama es una vista. Esa tensión se resuelve aquí porque condiciona el modo de cada fila.

## Goal

_Describe the concrete result this task must produce._

Una matriz de cobertura de todas las capacidades de spec2viz, con modo y condición de retiro por fila; la decisión sobre el papel del YAML de spec frente al grafo; y un gate comprobable de migración y retiro. Es un plan de cobertura: no declara nada como ya migrado.

## Scope

_State what is in scope and what is out of scope._

Dentro, una fila por cada capacidad de spec2viz, cada una con modo (migrar tal cual; reemplazar por otra arquitectura o experiencia con resultado equivalente; usar sldb directamente: lo que ya vive en SLDB se consume por su API, su CLI o sldb serve, sin envoltorio ni reexportación en specIR; migrado a sldb: las piezas de spec2viz que no son visuales ni de dominio, esto es SpecSync, from-graph, generador desde el AST de Python, modelos de spec por tipo de diagrama y emparejamiento de átomos, cuyo código pasa a sldb con sus pruebas portadas y que specIR consume desde allí) y condición verificable de retiro:
- Modelos de spec por tipo de diagrama: clase, secuencia, estado, componente, actividad, despliegue, matriz, reflexión; carga y validación de specs; export de JSON Schema de specs y de catálogos.
- Representación intermedia y compiladores por tipo de diagrama.
- Renderizadores: Mermaid, PlantUML, D2, BPMN y su visor, Vega, árbol, HTML de grafo, antonia-html y salida JSON.
- Linter de Mermaid.
- SpecSync: materializar un spec en el store como SpecDoc, SpecNodeDoc y RelationDoc, creando el RelationTypeDoc que falte y borrando lo que salió del spec.
- from-graph: compilar el grafo de un store o un snapshot en un spec de componentes.
- Generación de un spec de componentes desde el AST de Python.
- Catálogos: build (HTML autocontenido), sync, validate y serve con autoguardado de anotaciones; registro vistas.yml y stores jerárquicos de diagramas.
- NotationDoc, GlyphDoc, LinkDoc y PaletteDoc: list, validate, sync y view de notaciones; list, validate y sync de paletas, con la comprobación de contraste WCAG.
- Emparejamiento de átomos con elementos de diagrama y cobertura por vista.
- API Python pública y recursos empaquetados (plantillas HTML, bpmn-js, notaciones y paleta builtin).
- Comando about y la habilidad de uso de spec2viz instalada para agentes.
Dentro también: inventario de consumidores, con el archivo donde cada uno importa o invoca spec2viz: graph_ui (UIs/graph_ui/frontends/mindmap/sldb_adapter.py y su pyproject.toml), deskops (reglas de rutas en el módulo graph.desk_graph del paquete deskops, documentación de diagramas y la habilidad use-spec2viz) y los stores cuyo índice registra modelos spec2viz.sldb_models.
Dentro también, la decisión antes separada: la fuente semántica es el grafo de SLDB; decidir si el YAML de spec queda como formato de autoría e intercambio de forma permanente o solo durante la paridad; cómo se dibuja algo que todavía no existe en el grafo (diseño previo a la implementación); y qué pasa con los specs YAML existentes en los repos que usan spec2viz.
Fuera: migrar o implementar cualquier fila; extractores de otras tecnologías; análisis de impacto.

## Implementation Path

_Outline the expected implementation route or affected surface._

Fuentes: spec2viz/spec2viz/cli.py y los módulos del paquete; spec2viz/tests/ como definición de paridad; el plan absorber-spec2viz-y-modelos-ui de SLDB para lo que ya vive en SLDB. La matriz se escribe en el repo de specIR. Cada fila o grupo de filas se convierte después en una tarea de migración propia; esta tarea no migra nada. Propiedad de archivos compartidos: esta tarea crea docs/spec2viz/matriz-de-cobertura.md con todas las filas, su modo y su condición de retiro, sin evidencia de cumplimiento; la tarea final IR13 la actualiza después, añadiendo por fila la prueba que acredita la cobertura, una vez cerradas IR13a, IR13b, IR13c e IR13d.

Precisiones (preflight): revisión inventariada de spec2viz = commit 2de1056 (versión 0.2.0), cuya ayuda de CLI coincide con spec2viz/cli.py. Plan de SLDB = sldb/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/ (alcance.md, brief.md, decisiones.md). Tareas de sldb que migran: D1 task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo, D2 task-migrar-a-sldb-el-generador-de-spec-de-componentes-desde-un-grafo-y-desde-el-ast-de-python-d2-b4, D3 task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp, D4 task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4 (espejos task-espejo-sldb-* en este desk). Universo de repos para consumidores y specs existentes: los repos con .git bajo SLDB_1 (IR, deskops, pron, scion, sldb, spec2viz, UIs/graph_ui; sldb-runtime y deskops-runtime se auditan por su repo de origen) y todo store.yaml y store_index.yaml bajo SLDB_1. Atom de la decisión: se crea con deskops add atom en desk/atoms de este repo, five_wh_one_plus how, se añade a atoms de esta tarea, y como AtomDoc no tiene campo de estado, su título y su respuesta dicen que es propuesta pendiente de JP. El gate de retiro como lista comprobable vive en la matriz; docs/spec2viz/gate-de-retiro.md fija el procedimiento. Prueba de completitud: tests/test_matriz_cobertura_spec2viz.py.

## Validation

_List the checks required before this task can close._

- Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz aparecen en la matriz.
- Todos los módulos de compiladores, renderizadores, linters y generadores del paquete spec2viz aparecen en la matriz.
- Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada.
- Cada fila en modo reemplazar nombra el sustituto y la prueba que demostrará la equivalencia.
- Cada fila en modo usar sldb directamente cita la operación de la API pública de SLDB que la respalda, y no define ningún envoltorio en specIR.
- Cada fila en modo migrado a sldb cita la tarea de sldb que la migra (SpecSync, generador de spec desde grafo y AST, modelos de spec o emparejamiento de átomos) y las pruebas de spec2viz que se portan a sldb.
- Cada consumidor inventariado cita el archivo donde importa o invoca spec2viz.
- Existe un atom con la decisión sobre el YAML de spec frente al grafo, con las alternativas descartadas, la regla para diseño previo a la implementación y el destino de los specs existentes.
- El gate de retiro está escrito como lista comprobable: toda fila con su condición cumplida; la suite de spec2viz pasa contra specIR o tiene prueba equivalente declarada por fila reemplazada; ningún consumidor importa ni invoca spec2viz; ningún store registra modelos spec2viz.sldb_models.

## Done When

_Name the observable condition that makes the task complete._

La matriz, la decisión y el gate de retiro están escritos y revisados, y de la matriz se pueden derivar las tareas de migración sin volver a inventariar spec2viz.

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

FILE:desk/atoms/atom-entidad-aparición-proyección-y-notación-son-cosas-distintas.md
---
sldb:
  by: agent
  at: '2026-11-12T00:48:14Z'
  authority: generated
  via: save_document_payload
id: atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
title: Identidad semántica, aparición, proyección, notación y formato de autoría son
  cosas distintas
five_wh_one_plus: what
tags:
- system:specir
- topic:identidad
- topic:proyecciones
- layer:modelo
provenance: fundamentos_modelado_semantico_mcp.md
---

# Identidad semántica, aparición, proyección, notación y formato de autoría son cosas distintas

## Answer

La fuente semántica de specIR es el grafo tipado de SLDB. Se distinguen cinco cosas: (1) entidad semántica, lo que existe en el dominio o sistema (Post, PublishPost, POST /posts/{id}/publish), con una sola identidad en el grafo; (2) aparición, la presencia de esa entidad en una vista o diagrama; (3) proyección, el criterio que selecciona y organiza elementos y relaciones del grafo para una finalidad; (4) notación, las reglas para dibujarlos, que no redefinen su identidad ni su significado; (5) formato de autoría, el archivo en que alguien escribe o intercambia un diagrama. El YAML de spec de spec2viz es un formato de autoría e intercambio, válido al menos mientras dure la paridad con spec2viz: lo que declara entra al grafo y no constituye una segunda identidad. Dos diagramas pueden mostrar el mismo objeto sin duplicarlo. Si el YAML se conserva como formato permanente es una decisión pendiente, incluida en la candidata de cobertura de spec2viz.

FILE:desk/atoms/atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al.md
---
sldb:
  by: agent
  at: '2026-11-15T21:33:03Z'
  authority: generated
  via: create_document
id: atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al
title: 'Propuesta pendiente de JP: el YAML de spec queda como formato de autoría e
  intercambio subordinado al grafo'
five_wh_one_plus: how
tags:
- system:specir
- system:spec2viz
- topic:migracion
- topic:fuente-de-verdad
provenance: docs/decisiones/fuente-de-verdad-del-diagrama.md
---

# Propuesta pendiente de JP: el YAML de spec queda como formato de autoría e intercambio subordinado al grafo

## Answer

ESTADO: PROPUESTA, PENDIENTE DE DECISIÓN DE JP (no aceptada; el modelo de atom no tiene campo de estado). Premisa: la fuente semántica es el grafo de SLDB y un diagrama es una vista. Recomendación: (1) el YAML de spec se conserva de forma permanente como formato de autoría e intercambio, subordinado al grafo: al sincronizarlo (SpecSync en sldb, D1) sus elementos pasan a SpecNodeDoc, y un elemento que representa una entidad existente se ancla a ella con vínculo explícito (atoms/refs, sldb.api.matching, D4); ante conflicto gana el grafo y la diferencia es un hallazgo. (2) Los diagramas de lo que ya existe se producen como proyección del grafo (ViewDoc evaluado o sldb notations from-graph, D2); un YAML sobre algo existente vale solo como vista curada con elementos anclados. (3) Diseño previo a la implementación: lo que aún no existe se autora en el YAML como elemento sin ancla, SpecSync lo materializa como SpecNodeDoc propio del spec y no como entidad; cuando la entidad aparece en el grafo se ancla por vínculo explícito; un chequeo determinista lista los elementos sin ancla como diseño pendiente de implementar y reporta posibles anclas por emparejamiento difuso sin anclarlas solo. (4) Specs YAML existentes (spec2viz, sldb, graph_ui, pron, deskops): se quedan donde están sin reescritura ni borrado desde specIR; durante la paridad son fixtures que deben validar con sldb.api.notations.load_spec con los mismos errores; tras el retiro cada repo decide por su desk, a pedido de IR13, pasar a proyección los que describen código existente cuando la prueba de equivalencia lo muestre y mantener como YAML los de diseño. Alternativas descartadas: YAML como fuente y store derivado (duplica entidades, contradice la premisa); YAML solo durante la paridad (sin forma de dibujar diseño previo, obliga a reescribir specs vigentes, pierde el diff revisable); autorar siempre en el store sin YAML (pierde revisión por diff y rompe vistas.yml; reconsiderable si el MCP cubre autoría de vistas con revisión equivalente). Detalle: docs/decisiones/fuente-de-verdad-del-diagrama.md.

FILE:docs/spec2viz/matriz-de-cobertura.md
# Matriz de cobertura de spec2viz

Plan de cobertura para retirar spec2viz (tarea IR07). Cada capacidad de spec2viz tiene una fila con su
**modo** y su **condición de retiro**. Esta matriz **no acredita nada**: no hay columna de evidencia y
ninguna fila se da por cumplida. La tarea final IR13 añade por fila la prueba que acredita la cobertura
(después de IR13a, IR13b, IR13c e IR13d) y es la única que puede marcar una fila como cumplida.

- Revisión inventariada de spec2viz: commit `2de1056` del repo `spec2viz` (versión 0.2.0 en su
  `pyproject.toml`). La ayuda del CLI instalado (`spec2viz --help` y la de cada subgrupo) coincide con
  `spec2viz/spec2viz/cli.py` de esa revisión.
- Revisión de sldb consultada: rama main de `sldb` en `641ecdfa`. Plan de sldb que absorbe lo genérico:
  `sldb/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/` (`alcance.md`, `brief.md`, `decisiones.md`).
- Decisión vigente (JP, 2026-11-15): lo genérico va a sldb; specIR es adaptador y mapeo de dominio y
  conserva la capa visual (compiladores en IR11, renderers en IR12).
- La decisión sobre el papel del YAML de spec frente al grafo está en
  `docs/decisiones/fuente-de-verdad-del-diagrama.md` y en el atom
  `atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`. Es una **propuesta pendiente de JP**;
  ninguna fila de esta matriz depende de que se acepte en un sentido u otro salvo las marcadas con †.
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
| SV-C05 | Vega (matriz) | `spec2viz/renderers/vega.py` | migrar tal cual | IR12 | Casos vega de `tests/test_renderers.py` y test_render_to_file_vega de `tests/test_api.py`. |
| SV-C06 | BPMN (XML con DI) | `spec2viz/renderers/bpmn.py` | migrar tal cual | IR12 | `tests/test_bpmn.py` (26), parte XML y DI, portado y en verde. |
| SV-C07 | Visor BPMN offline (bpmn-js embebido, leyenda, metadata, panel) | `spec2viz/renderers/bpmn_viewer.py` | migrar tal cual | IR12 | Casos del visor de `tests/test_bpmn.py`; la prueba de recursos de IR12 abre el HTML sin recursos externos faltantes. |
| SV-C08 | Paleta BPMN in Color compartida por renderer y visor | `spec2viz/renderers/bpmn_palette.py` | migrar tal cual | IR12 | Mismos colores en XML y visor sobre los fixtures de `tests/test_bpmn.py`. |
| SV-C09 | Árbol (HTML colapsable) | `spec2viz/renderers/tree.py` | migrar tal cual | IR12 | Casos tree de `tests/test_renderers.py` portados. |
| SV-C10 | HTML de grafo (DOM puro, sin CDN) | `spec2viz/renderers/graph_html.py` | migrar tal cual | IR12 | Casos graph de `tests/test_renderers.py` y test_render_to_file_component de `tests/test_api.py`; abre desde file:// sin recursos externos (prueba de recursos de IR12). |
| SV-C11 | antonia-html | `spec2viz/renderers/antonia.py` | migrar tal cual | IR12 | Casos antonia de `tests/test_renderers.py` y test_render_antonia_html de `tests/test_cli.py`. |
| SV-C12 | Salida JSON (`JsonRenderer`, artefacto `.artifact.json`) | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`json_out`) | test_render_json_reflection_artifact de `tests/test_cli.py` portado y en verde. |
| SV-C13 | Backends UML de sintaxis para el ClassIR (mermaid y plantuml de clases) | `spec2viz/renderers/class_diagram.py` | migrar tal cual | IR12 (falta en la lista de archivos de IR12: ver pendientes) | Casos de clases de `tests/test_renderers.py`, `tests/test_class_diagram.py` y `tests/test_class_packages.py` con render. |
| SV-C14 | Mermaid desde una vista resuelta (glifo, forma, keyword, compartimentos, estilo) | `spec2viz/renderers/view_mermaid.py` | migrar tal cual | IR12, consumiendo `sldb.api.notations.resolve_view` (falta en la lista de archivos de IR12: ver pendientes) | `tests/test_catalog_resolved_views.py` (8) portado y en verde contra la vista resuelta de sldb. |
| SV-C15 | Prueba de regresión de render a archivo | `spec2viz/__init__.py` (`render_to_file`) | migrar tal cual | IR12 e IR13d | `tests/test_rendering_bug.py` (1) portado y en verde. |

### D. Linter

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-D01 | Linter de Mermaid (heurísticas y pasada real con mmdc si está) | `spec2viz/linters/mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/lint_mermaid.py`) | `tests/test_mermaid_mmdc.py` (4) portado y en verde; los mismos hallazgos que spec2viz sobre los fixtures de lint (prueba de lint de IR12). |

### E. Sincronización al store (SpecSync)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-E01 | SpecSync: materializar un spec como SpecDoc, SpecNodeDoc y RelationDoc, crear el RelationTypeDoc que falte y borrar lo que salió del spec; informe (`format_report`) | `spec2viz/sldb_sync.py` | migrado a sldb | D1: `SpecSync`, `sync_spec` en `sldb.api.notations`; `sldb notations sync --spec`. Reutiliza `StoreWriter` y `SyncReport` de sldb | `tests/test_sldb_sync.py` (16) portado a sldb, contra store real y sin mocks, en verde; informe igual campo a campo al de spec2viz sobre los mismos specs (D1); specIR llama a la API de sldb (IR13a). |
| SV-E02 | Sincronización de notaciones y paletas al store (`NotationSync`, `PaletteSync`, `format_notation_report`) | `spec2viz/sldb_sync.py` | usar sldb directamente | `sldb.api.notations.NotationSync`, `PaletteSync`, `sync_notation`, `sync_palette`; CLI `sldb notations sync --notation/--palette` | Los casos de notación y paleta de `tests/test_sldb_sync.py` y `tests/test_style_palette.py` que sincronizan pasan llamando a la API de sldb, sin envoltorio en specIR. |

### F. Generación de specs

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-F01 | from-graph: compilar el grafo de un store (edge index) o un snapshot node-link en un spec de componentes | `spec2viz/graph_import.py` | migrado a sldb | D2: `component_spec_from_graph` en `sldb.api.notations`; `sldb notations from-graph --snapshot/--store` | `tests/test_graph_import.py` (21) portado a sldb y en verde; todo spec generado valida con el modelo de componentes de D3. |
| SV-F02 | Generar un spec de componentes desde el AST de Python | `spec2viz/generators/python_ast.py` | migrado a sldb | D2: `component_spec_from_python` sobre `sldb.code.scan_tree`, `write_component_spec`; `sldb notations from-graph --python` | spec2viz no tiene pruebas de este generador: la condición es la prueba nueva de D2 que compara con `generate_python_ast_spec` de spec2viz sobre un árbol pequeño (mismos módulos, clases y relaciones defines) y valida con el modelo de D3. |

### G. Catálogos

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-G01 | Construcción del catálogo HTML autocontenido desde un `vistas.yml` o un store de stores (marca, subtítulo, plantilla local, `project.yml`, secciones HTML, anchors únicos) | `spec2viz/orchestrator.py` | migrar tal cual | IR13b con los renderers de IR12 | test_build_command* (7), test_catalog_build_alias_matches_legacy_build y test_build_command_reports_errors de `tests/test_cli.py` portados y en verde; mismas vistas, categorías y navegación que spec2viz sobre el fixture (IR13b). |
| SV-G02 | Registro `vistas.yml` y stores jerárquicos de diagramas: regla de rutas de `src`, `mmd`, `specs` y `notation` | `spec2viz/catalog_paths.py` | migrar tal cual | IR13b | `tests/test_catalog_paths.py` (9) portado y en verde. |
| SV-G03 | Vistas del catálogo desde la vista resuelta (misma fuente que graph_ui) | `spec2viz/catalog_views.py` | migrar tal cual | IR13b, consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde (compartido con SV-C14). |
| SV-G04 | Sincronización del catálogo al store (`catalog sync`: cada spec del `vistas.yml` con su notación y metadata) | `spec2viz/sldb_sync.py` (`sync_catalog`) | migrado a sldb | D1: `sync_catalog`; `sldb notations sync --catalog` (con `--prune` para borrar los SpecDoc que salieron) | `tests/test_catalog_notation.py` (6) portado a sldb y en verde; no escribe nada si una vista falla (IR13b). |
| SV-G05 | Validación del catálogo (`catalog validate`: specs existen y validan, notaciones del tipo correcto) | `spec2viz/sldb_sync.py` (`check_catalog`) | migrado a sldb | D1: `check_catalog`; `sldb notations sync --catalog --check` | Casos de validación de `tests/test_catalog_notation.py` portados a sldb; mismos errores tipados que spec2viz (IR13b). |
| SV-G06 | Servir el catálogo en local con autoguardado de anotaciones (`catalog serve`) | `spec2viz/cli.py` (`catalog_serve`) | reemplazar | Sustituto: `sldb serve` (lectura de documento por id y escritura con guarda de hash, comprobado por D4 paso 7) más el JS del catálogo de specIR (IR13b) | Prueba de equivalencia: IR13b demuestra que una anotación hecha con el catálogo servido por `sldb serve` queda guardada y reaparece al recargar. Si D4 concluye que `sldb serve` no alcanza, la fila no se cumple hasta que sldb resuelva la nota `serve/annotation-autosave-gap`. |
| SV-G07 | Inyección de átomos en el HTML del catálogo (`render_deskops`, `build_deskops`, `split_shared_atoms`, adaptador `CatalogItem`) | `spec2viz/deskops.py` | migrar tal cual | IR13b (capa visual; D4 lo deja fuera de sldb) | `tests/test_deskops.py` (7) y, de `tests/test_atoms_matching.py`, test_split_shared_atoms_emits_repeated_payload_once y test_catalog_build_embeds_atoms_once_and_honors_atoms_tag, portados y en verde. |
| SV-G08 | Plantilla HTML del catálogo, incluido el emparejamiento difuso en el navegador (`findAtomData`, `normKey`) y las pestañas por átomo | `spec2viz/templates/default.html` | migrar tal cual | IR12 (`src/specir/visual/templates/default.html`) e IR13b | Los casos de `tests/test_atoms_matching.py` que ejecutan la plantilla con node y test_tabs_follow_the_target_atom portados y en verde; `label_key` de D4 sigue coincidiendo con `normKey`. |

### H. Notaciones, paletas y estilo (usar sldb directamente)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-H01 | Modelo, carga y validación de notaciones (NotationDoc, GlyphDoc, LinkDoc en YAML; `where` en la gramática de `sldb find --where`) | `spec2viz/notation.py` | usar sldb directamente | `sldb.notations.load_notation`, `sldb.notations.NotationSpec` | Los casos de `tests/test_notation.py` (14) pasan contra `sldb.notations` sin envoltorio en specIR. |
| SV-H02 | Notaciones builtin (8) y notación por defecto por tipo | `spec2viz/notations/*.yml`, `DEFAULT_NOTATIONS` | usar sldb directamente | `sldb.notations.builtin_notations`, `sldb.notations.DEFAULT_NOTATIONS` | Las 8 notaciones de spec2viz (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence) aparecen en `sldb notations list` y su contenido valida igual. |
| SV-H03 | Vista resuelta de un spec (glifo por nodo, link por relación, leyenda) y de documentos sin SpecDoc | `spec2viz/notation_view.py` (`resolve_view`, `resolve_documents`) | usar sldb directamente | `sldb.api.notations.resolve_view`, `sldb.api.notations.resolve_documents`; CLI `sldb notations view` y `sldb notations resolve` | `tests/test_notation_view.py` (11) y `tests/test_view_contract_resolved.py` (2) pasan contra la API de sldb; graph_ui ya no importa `spec2viz.notation_view` (gate G4). |
| SV-H04 | Modelo, carga y validación de paletas, con contraste WCAG (trazo ≥ 3:1, texto ≥ 4.5:1, forma+icono distintos por kind) | `spec2viz/palette.py` | usar sldb directamente | `sldb.notations.load_palette`, `sldb.notations.PaletteSpec`, `sldb.notations.contrast` | Los casos de paleta y contraste de `tests/test_style_palette.py` pasan contra `sldb.notations`. |
| SV-H05 | Paleta builtin `default` | `spec2viz/palettes/default.yml` | usar sldb directamente | `sldb.notations.builtin_palettes` (`src/sldb/notations/palettes/default.yml`) | `sldb notations list` la lista y su contenido valida igual. |
| SV-H06 | Estilo con una sola precedencia (glifo > `style.kinds` del spec > paleta) | `spec2viz/styling.py` | usar sldb directamente | `sldb.notations.resolve_style`, `sldb.notations.resolve_line_color` | Los casos de precedencia de `tests/test_style_palette.py` pasan contra `sldb.notations`. |

### I. Emparejamiento de átomos con elementos de diagrama

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-I01 | Emparejamiento explícito (`atoms:` en el elemento), alias por título y etiquetas, filtro por tags, avisos y modo estricto (`UnknownAtomError`) | `spec2viz/deskops.py` | migrado a sldb | D4: `sldb.api.matching` (módulos de claves y alias, resolución explícita) | Portados a sldb y en verde: de `tests/test_atoms_matching.py` test_filter_atoms_payload_by_full_tag_or_value; de `tests/test_explicit_atoms.py` test_build_exposes_explicit_map_by_label_and_id, test_unknown_atom_is_warning_unless_strict, test_fully_explicit_view_embeds_no_fuzzy_payload, test_partially_explicit_view_keeps_fuzzy_payload y test_atoms_linked_from_explicit_are_embedded_one_level. |
| SV-I02 | Emparejamiento difuso de átomos con elementos | `spec2viz/templates/default.html` (en el navegador) | migrado a sldb | D4: `DocumentIndex.rank` sobre `Matcher`/`DifflibMatcher` con alias (sin matcher nuevo); el JS del navegador sigue en SV-G08 | Prueba nueva de D4 de emparejamiento difuso con alias en verde, y SV-G08 cumplida. |
| SV-I03 | Referencias `refs: [Model:name]` por elemento hacia documentos sldb y aristas de átomos (`collect_explicit_refs`, `build_explicit_refs`, `attach_atom_edges`) | `spec2viz/deskops.py` | migrado a sldb | D4 (resolución de refs) | `tests/test_refs.py` (14) en verde: los casos de resolución contra sldb (D4) y los de schema y CLI contra specIR (IR12, IR13d). D4 no lista hoy `tests/test_refs.py` entre sus pruebas portadas: ver pendientes. |
| SV-I04 | Cobertura de átomos por vista | `spec2viz/deskops.py` (`build_coverage_by_view`) | migrado a sldb | D4 (módulo de cobertura) | Prueba de cobertura de D4 en verde y los casos de cobertura de `tests/test_deskops.py` portados. |
| SV-I05 | Descubrimiento y carga del store de átomos (`SldbAtomResolver`) | `spec2viz/deskops.py` | usar sldb directamente | `sldb.api.stores.open_store` y lectura de documentos y del edge index de `sldb.api` | Las pruebas de SV-I01 a SV-I04 pasan sin `SldbAtomResolver`. |

### J. API Python pública, recursos empaquetados, about y habilidad

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-J01 | `spec2viz.load` y `spec2viz.validate` | `spec2viz/__init__.py` | migrado a sldb | D3: `sldb.api.notations.load_spec`, `validate_spec` | test_load_* (6), test_validate_passes y test_validate_fails de `tests/test_api.py` pasan contra la API de sldb. |
| SV-J02 | `compile_ir`, `render`, `json_schema`, `write_json_schema` | `spec2viz/__init__.py` | migrar tal cual | IR13d (API pública de la capa visual de specIR) | El resto de `tests/test_api.py` (27 en total) portado contra la API de specIR y en verde. |
| SV-J03 | `render_to_file` con cabecera de procedencia (`with_provenance`, `provenance_header`, `provenance_text`) y salida BPMN doble (`.bpmn` y `.bpmn.html`) | `spec2viz/__init__.py` | migrar tal cual | IR13d | test_render_to_file_* (7) de `tests/test_api.py` y test_rendered_text_projections_carry_a_provenance_header de `tests/test_cli.py` portados; la cabecera nombra el comando de specIR que valida. |
| SV-J04 | Recurso empaquetado: bpmn-js vendorizado | `spec2viz/templates/vendor/bpmn-js/` | migrar tal cual | IR12 (prueba de recursos) | El visor BPMN abre offline (SV-C07) y `tests/test_packaging.py` portado (incluido test_examples_render_successfully) en verde. |
| SV-J05 | Recurso empaquetado: plantilla HTML del catálogo | `spec2viz/templates/default.html` | migrar tal cual | IR12 | Ver SV-G08; la plantilla viaja en el paquete instalado de specIR (prueba de recursos de IR12). |
| SV-J06 | Recursos empaquetados: notaciones y paleta builtin | `spec2viz/notations/`, `spec2viz/palettes/` | usar sldb directamente | Builtins de sldb (`src/sldb/notations/builtin/`, `src/sldb/notations/palettes/`) vía `sldb.notations.builtin_notations` y `builtin_palettes` | specIR no empaqueta notaciones ni paletas; SV-H02 y SV-H05 cumplidas. |
| SV-J07 | Punto de entrada `spec2viz` y empaquetado (instala y arranca) | `pyproject.toml` (`[project.scripts]`), `spec2viz/cli.py` (`main`) | reemplazar | Sustituto: el comando de specIR (IR13d) | Prueba de IR13d: el paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado; test_primary_cli_still_exposes_commands de `tests/test_packaging.py` portado. |
| SV-J08 | Comando about (dónde viven los diagramas y cómo llega el flujo al HTML) | `spec2viz/cli.py` (`about`) | migrar tal cual | IR13d | El comando equivalente de specIR existe y lo invoca la prueba de CLI de IR13d; su texto nombra los comandos de specIR y de sldb que sustituyen a los de spec2viz. |
| SV-J09 | Habilidad de agente use-spec2viz | `.pi/skills/use-spec2viz/SKILL.md` (copia distinta en `deskops/.opencode/skills/use-spec2viz/SKILL.md`) | reemplazar | Sustituto: `skills/use-specir/SKILL.md` (IR13d) | Prueba de IR13d que extrae los comandos que nombra la habilidad y los invoca con ayuda; la habilidad no nombra comandos de spec2viz. |

### K. Comandos y subgrupos del CLI

Una fila por cada entrada que lista la ayuda (`spec2viz --help` y la de cada subgrupo). La correspondencia
detallada la escribe IR13d en `docs/spec2viz/correspondencia-cli.md`. Cuando la capacidad vive en sldb, el
equivalente es el comando de sldb y specIR no define subcomando propio.

| ID | Comando | Modo | Equivalente | Condición de retiro |
|---|---|---|---|---|
| SV-K01 | `spec2viz about` | migrar tal cual | Comando about de specIR (IR13d) | SV-J08. |
| SV-K02 | `spec2viz build` (alias de `catalog build`) | migrar tal cual | Alias en el comando de specIR (IR13d) | SV-G01; test_catalog_build_alias_matches_legacy_build portado. |
| SV-K03 | `spec2viz catalog` (subgrupo) | migrar tal cual | Subgrupo catalog de specIR con build y schema; sync, validate y serve remiten a sldb | SV-K04 a SV-K08 cumplidas. |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | specIR (IR13b, IR13d) | SV-G01. |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A16. |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve` sobre el store del catálogo (IR13b) | SV-G06. |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` (D1) | SV-G04. |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` (D1) | SV-G05. |
| SV-K09 | `spec2viz diagram` (subgrupo) | migrar tal cual | Subgrupo diagram de specIR con render, lint y schema (y validate, ver SV-K16); sync, from-graph y generate remiten a sldb | SV-K10 a SV-K16 cumplidas. |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot/--store` (D2) | SV-F01; test_cli_from_graph_* (5) y test_cli_from_graph_module_prefix reescritos contra el comando de sldb (D2). |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python` (D2) | SV-F02. |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | specIR (IR12, IR13d) | SV-D01. |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | specIR (IR12, IR13d) | test_render_* de `tests/test_cli.py` portados; SV-C01 a SV-C12. |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A15. |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec` (D1) | SV-E01. |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb | Lógica en sldb (`load_spec`, `validate_spec`, D3); hoy sldb no tiene comando que valide un spec: o sldb lo añade (pedido por su desk) o el comando de specIR lo invoca sin redefinir nada (IR13d) | test_validate_valid, test_validate_invalid y test_validate_all_types de `tests/test_cli.py` portados contra el comando elegido; SV-A11 y SV-A12. |
| SV-K17 | `spec2viz lint` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K12. |
| SV-K18 | `spec2viz notation` (subgrupo) | usar sldb directamente | `sldb notations` | SV-K19 a SV-K22 cumplidas. |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | SV-H02. |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | SV-E02. |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation`; sldb no tiene hoy comando de validación de notaciones (ver pendientes) | SV-H01 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view` | SV-H03. |
| SV-K23 | `spec2viz palette` (subgrupo) | usar sldb directamente | `sldb notations` (`list`, `sync --palette`) | SV-K24 a SV-K26 cumplidas. |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` (incluye `builtin_palettes`) | SV-H05. |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | SV-E02. |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (con contraste WCAG); sldb no tiene hoy comando de validación de paletas (ver pendientes) | SV-H04 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. |
| SV-K27 | `spec2viz render` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K13. |
| SV-K28 | `spec2viz schema` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K14. |
| SV-K29 | `spec2viz validate` (alias) | migrado a sldb | Igual que SV-K16 | SV-K16. |
| SV-K30 | Ayuda raíz con taxonomía (diagram, catalog) y lista de renderers | migrar tal cual | Ayuda del comando de specIR (IR13d) | test_help_mentions_taxonomy_groups_and_renderers de `tests/test_cli.py` portado. |

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
| deskops | `deskops/deskops/graph/desk_graph.py:75` (regla de rutas `FileRule(kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"))`) | regla de rutas del grafo del desk | decidir la ruta de specs según la decisión del YAML (†); pedido al desk de deskops |
| deskops | `deskops/desk/drawer/plans/workspace-documental/render_diagram.py:7` y `:9` (`spec2viz diagram validate` y `diagram render`) | invocación | comandos de specIR (SV-K13, SV-K16) |
| deskops | `deskops/docs/diagrams/README.md` y los `.md`/`.mmd` de `deskops/docs/diagrams/` que nombran a spec2viz | documentación de diagramas (no cuenta como dependencia para IR13; se regenera con specIR) | renderers de specIR |
| deskops | `deskops/.opencode/skills/use-spec2viz/SKILL.md`; `deskops/.claude/skills/deskops-workflow/SKILL.md` y `references/spec2viz-cli.md` (instruyen a agentes a invocar `spec2viz`) | habilidad de agente | `skills/use-specir/SKILL.md` (SV-J09) |
| pron | `pron/docs/spec2viz/build.py:22-24` (`spec2viz diagram validate`, `diagram render --backend mermaid`, `catalog build`) | invocación | comandos de specIR (SV-K13, SV-K16, SV-K04) |
| sldb | `sldb/docs/architecture/spec2viz/vistas.yml` y sus specs (`current-*.yml`, `python-ast.yml`) | registro de catálogo que construye `spec2viz catalog build` | catálogo de specIR (SV-G01) |
| sldb | `sldb/contracts/identity.toml:299` (`consumers = [..., "spec2viz", ...]`) | configuración de contrato | quitar spec2viz de la lista al retirarlo |
| IR (specIR) | `IR/tests/conftest.py:24` y `:80` (federa el store `spec2viz/.sldb`), `IR/tests/test_mcp_extension.py:24` (`SPEC_STORE = "spec2viz"`) | lectura del store de spec2viz en pruebas | store con modelos de sldb (G5) o fixture propio |
| store `spec2viz/.sldb` | `spec2viz/.sldb/store.yaml:44-57`, `spec2viz/.sldb/core/store_index.yaml:141-194`, `spec2viz/.sldb/core/models/{SpecDoc,SpecNodeDoc,NotationDoc,GlyphDoc,LinkDoc,PaletteDoc,ViewDoc}.yaml` | modelos `spec2viz.sldb_models` registrados | `sldb.models.notation.*` (SV-A17) |

Es el único store bajo `SLDB_1/` cuyo índice registra `spec2viz.sldb_models`.

Specs YAML existentes que afecta la decisión del YAML (†): `spec2viz` (44: `tests/fixtures/`,
`docs/architecture/spec2viz/`, `examples/`), `sldb` (46: `tests/fixtures/`, `docs/architecture/`),
`UIs/graph_ui` (24: `tests/fixtures/`, `docs/representacion/`), `pron` (4: `docs/spec2viz/specs/`),
`deskops` (1: `desk/drawer/plans/workspace-documental/`). Conteo de archivos con `type:` de uno de los
ocho tipos en la raíz, sin `.sldb/`, `build/` ni entornos.

## Pendientes de derivación

Lo que esta matriz deja abierto y debe convertirse en tarea o pedido (no lo resuelve IR07):

1. Filas «usar sldb directamente» (SV-A17, SV-E02, SV-H01 a SV-H06, SV-I05, SV-J06, SV-K18 a SV-K26):
   con IR13c retirada, ninguna tarea porta hoy `tests/test_notation.py`, `tests/test_notation_view.py`,
   `tests/test_view_contract_resolved.py`, `tests/test_style_palette.py` ni `tests/test_view_doc.py`
   contra sldb. La prueba de paridad la aporta IR13 (prueba en specIR que llama a sldb sin envoltorio) o
   una tarea nueva derivada de estas filas.
2. SV-K21 y SV-K26: sldb no tiene comando para validar una notación o una paleta por nombre o ruta.
   Pedido al desk de sldb (`deskops message send --to sldb`) pendiente.
3. SV-K16 y SV-K29: decidir si la validación de un spec por CLI la da sldb (pedido a su desk) o el comando
   de specIR sobre `load_spec`/`validate_spec`.
4. SV-I03: D4 no lista `tests/test_refs.py` entre sus pruebas portadas; pedir a sldb que lo incluya o
   asignar la parte de resolución a IR13b.
5. SV-C13 y SV-C14: la lista de archivos de IR12 no incluye los backends UML de clases ni el mermaid desde
   vista resuelta; IR12 debe añadirlos.
6. Consumidores: pedidos de migración a los desks de graph_ui, deskops, pron y sldb (los emite IR13).

## Gate de retiro

Lista comprobable. spec2viz solo se retira cuando **todos** los ítems se cumplen; el procedimiento está en
`docs/spec2viz/gate-de-retiro.md` y lo evalúa IR13.

- [ ] **G1. Filas cumplidas.** Toda fila SV-* de esta matriz tiene su condición de retiro cumplida y la
  prueba que lo acredita citada por IR13 en la fila (ninguna fila sin prueba; ninguna dice descartado ni
  fuera de alcance).
- [ ] **G2. Suite de spec2viz.** Cada caso de cada archivo de `spec2viz/tests/` pasa contra specIR o
  contra sldb (portado), o pertenece a una fila en modo reemplazar cuya prueba equivalente está declarada y
  pasa. La tabla «Pruebas de spec2viz por fila» no deja archivo sin fila.
- [ ] **G3. CLI.** Cada comando y subgrupo de la ayuda de spec2viz (filas SV-K*) tiene equivalente que
  existe y una prueba lo invoca (`docs/spec2viz/correspondencia-cli.md` de IR13d).
- [ ] **G4. Consumidores.** Ningún consumidor del inventario importa ni invoca spec2viz: cero
  `import spec2viz`/`from spec2viz`, cero dependencias declaradas (pyproject, requirements, CI), cero
  invocaciones del comando `spec2viz` en código, scripts o configuración ejecutable, y ninguna habilidad de
  agente que instruya a invocarlo. El comprobador de IR13 sale con código distinto de cero si encuentra una.
- [ ] **G5. Stores.** Ningún store del universo registra modelos `spec2viz.sldb_models` en su
  `store.yaml`, su `store_index.yaml` ni sus `core/models/*.yaml`.
- [ ] **G6. specIR limpio.** Ningún módulo bajo `src/specir/` importa spec2viz (prueba de imports) y specIR
  no define envoltorios de lo que se usa de sldb directamente.
- [ ] **G7. Decisión del YAML.** La decisión sobre el YAML de spec frente al grafo
  (`docs/decisiones/fuente-de-verdad-del-diagrama.md`) está aceptada por JP y las filas marcadas con †
  están alineadas con ella.

FILE:docs/spec2viz/gate-de-retiro.md
# Gate de retiro de spec2viz: procedimiento

La lista comprobable del gate (G1 a G7) está en la sección «Gate de retiro» de
`docs/spec2viz/matriz-de-cobertura.md`; este documento no la repite, solo fija quién la evalúa, en qué
orden y qué pasa si falla.

## Quién y cuándo

- Lo evalúa la tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`), una
  vez cerradas IR11, IR12, IR13a, IR13b, IR13d y las tareas de sldb D1 a D4.
- IR13 es la única que escribe evidencia en la matriz (la prueba que acredita cada fila) y el acta de
  retiro `docs/spec2viz/acta-de-retiro.md`.
- Archivar o borrar el repo spec2viz es decisión de su dueño una vez cumplido el gate; ni IR07 ni IR13 lo
  hacen.

## Orden de evaluación

1. **G7** primero: si la decisión del YAML no está aceptada por JP, el gate no se evalúa.
2. **G6** (specIR limpio): prueba de imports de specIR.
3. **G1, G2 y G3** (filas, suite y CLI): por cada fila, ejecutar la prueba citada; la tabla «Pruebas de
   spec2viz por fila» no puede dejar un archivo de `spec2viz/tests/` sin fila ni un caso sin portar o sin
   prueba equivalente declarada.
4. **G4 y G5** (consumidores y stores): el comprobador de IR13 recorre en solo lectura exactamente el
   universo del «Inventario de consumidores» de la matriz más el repo de specIR, y lista cada dependencia
   remanente con repo o store, ruta, línea y clase.

## Si falla

- Cualquier ítem en falso: el comprobador sale con código distinto de cero y el retiro no se declara.
- Una dependencia remanente en otro repo no se corrige desde specIR: se pide al desk de ese repo
  (`deskops message send --to <repo>`) y se registra como evidencia pendiente.
- Una fila cuya condición resulta imposible se reescribe en la matriz con aprobación de JP; nunca se
  marca como descartada sin prueba.

FILE:docs/decisiones/fuente-de-verdad-del-diagrama.md
# Fuente de verdad del diagrama: el grafo de SLDB y el papel del YAML de spec

**Estado: propuesta, pendiente de decisión de JP.** No está aceptada. El atom que la registra en el desk
es `atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`;
el modelo de atom de deskops no tiene campo de estado, así que el
estado va en el título y en la respuesta. Cuando JP decida, se actualiza este documento y el atom, y el
ítem G7 del gate de retiro (`docs/spec2viz/matriz-de-cobertura.md`) pasa a comprobable.

## Contexto

Conviven dos modelos de diagrama:

- **spec2viz**: el YAML del spec es la fuente; el store es derivado (`spec2viz diagram sync` materializa
  el spec como SpecDoc, SpecNodeDoc y RelationDoc).
- **specIR**: la fuente semántica es el grafo de SLDB (entidades extraídas o autoradas, sus aristas); un
  diagrama es una **vista** (aparición de entidades bajo una notación), no una segunda copia de las
  entidades (atom `atom-entidad-aparición-proyección-y-notación-son-cosas-distintas`).

Dado que la fuente semántica es el grafo (premisa fijada por la tarea IR07), queda por decidir el papel
del YAML de spec, cómo se dibuja lo que aún no existe en el grafo y qué pasa con los specs existentes.

## Recomendación

1. **El YAML de spec se conserva de forma permanente como formato de autoría e intercambio, subordinado
   al grafo.** Es la forma revisable en un diff de autorar una vista o un diseño. No es fuente de las
   entidades: al sincronizarlo (SpecSync, D1: `sldb notations sync --spec`) sus elementos pasan a
   SpecNodeDoc del store, y un elemento que representa una entidad existente se ancla a ella con un
   vínculo explícito (`atoms:`/`refs:` por elemento, resuelto por `sldb.api.matching`, D4). Ante un
   conflicto entre el YAML y el grafo, gana el grafo y la diferencia se reporta como hallazgo; el YAML no
   sobrescribe documentos de entidad.
2. **Los diagramas de lo que ya existe se producen como proyección del grafo** (ViewDoc evaluado por
   `sldb.api.notations.evaluate_projection_view`, o un spec de componentes generado con
   `sldb notations from-graph`, D2), no se escriben a mano. Un YAML autorado para algo que ya está en el
   grafo es válido solo como vista curada (selección, orden, agrupación, notación), y sus elementos van
   anclados.
3. **Regla para diseño previo a la implementación.** Lo que aún no existe en el grafo se autora en el YAML
   del spec como elemento **sin ancla**. SpecSync lo materializa como SpecNodeDoc propio del spec (no como
   entidad del dominio). Cuando la implementación aparece en el grafo (un extractor o una autoría crea la
   entidad), el elemento se ancla por vínculo explícito y el diagrama pasa a validarse contra el grafo.
   Un chequeo determinista lista los elementos sin ancla de cada spec como «diseño pendiente de
   implementar»; no es error, es estado visible. Un elemento sin ancla cuyo nombre empareja con una
   entidad existente (emparejamiento difuso de D4) se reporta como «posible ancla» para que alguien lo
   confirme; nunca se ancla solo.
4. **Destino de los specs YAML existentes.** Se quedan donde están, sin reescritura masiva ni borrado
   desde specIR:
   - Durante la paridad son fixtures: los de `spec2viz/tests/fixtures/`, `spec2viz/examples/` y
     `spec2viz/docs/architecture/spec2viz/` se portan como fixtures de las pruebas de paridad (IR11,
     IR12, D3) y deben validar con `sldb.api.notations.load_spec` con los mismos errores tipados.
   - Tras el retiro, cada repo (sldb, graph_ui, pron, deskops; inventario en la matriz) decide por su
     desk, a pedido de IR13: los specs que describen código ya presente en el grafo pueden pasar a
     proyección cuando la prueba de equivalencia lo muestre; los de diseño se mantienen como YAML,
     validados con sldb y sincronizados con `sldb notations sync --spec`.
   - La ruta `docs/architecture/spec2viz` que reconoce el grafo del desk de deskops
     (`deskops/deskops/graph/desk_graph.py:75`) se renombra o generaliza por pedido al desk de deskops;
     specIR no la toca.

## Alternativas descartadas

- **El YAML como fuente y el store como derivado (el modelo de spec2viz tal cual).** Duplica entidades:
  la misma clase o componente existe como entidad del grafo y como nodo del spec, y nada obliga a que
  coincidan. Contradice la premisa de que la fuente semántica es el grafo.
- **El YAML solo durante la paridad y después solo proyecciones.** Deja sin forma de dibujar un diseño
  antes de implementarlo, y obliga a reescribir o borrar specs vigentes en cinco repos sin beneficio
  verificable. También pierde el formato de intercambio revisable en diffs.
- **Autorar siempre en el store (CLI o MCP de sldb) sin YAML.** Viable para agentes, pero quita la
  revisión por diff de un archivo y rompe los flujos de catálogo (`vistas.yml`) y los specs existentes. Se
  puede reconsiderar si el MCP llega a cubrir la autoría de vistas con revisión equivalente.

## Efecto sobre la matriz

Las filas marcadas con † en `docs/spec2viz/matriz-de-cobertura.md` dependen de esta decisión: el
inventario de specs existentes y la regla de rutas de deskops. El resto de las filas no cambia de modo
con ninguna de las alternativas.

FILE:tests/test_matriz_cobertura_spec2viz.py
"""The spec2viz coverage matrix (IR07) lists every capability that the retirement gate has to cover.

Completeness is checked against spec2viz itself: every command and subgroup of its CLI help, every
module of its compilers, renderers, linters and generators, and every file of its test suite has a
row in `docs/spec2viz/matriz-de-cobertura.md`, and every row has one of the four coverage modes.

The CLI tree comes from click when spec2viz is importable, and otherwise from the decorators in
`spec2viz/cli.py` (specIR never depends on spec2viz, so the source is the usual path)."""

from __future__ import annotations

import ast
import importlib
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "docs" / "spec2viz" / "matriz-de-cobertura.md"
SPEC2VIZ = REPO.parent / "spec2viz"
PACKAGE = SPEC2VIZ / "spec2viz"
SUBPACKAGES = ("compilers", "renderers", "linters", "generators")
MODES = ("migrar tal cual", "reemplazar", "usar sldb directamente", "migrado a sldb")

pytestmark = pytest.mark.skipif(not (PACKAGE / "cli.py").is_file(), reason=f"spec2viz sources not found at {SPEC2VIZ}")


def commands_from_click() -> set[str] | None:
    try:
        main = importlib.import_module("spec2viz.cli").main
    except ImportError:
        return None
    paths: set[str] = set()

    def walk(group, prefix: str) -> None:
        for name, command in group.commands.items():
            path = f"{prefix} {name}"
            paths.add(path)
            if hasattr(command, "commands"):
                walk(command, path)

    walk(main, "spec2viz")
    return paths


def commands_from_source() -> set[str]:
    """Each `@<parent>.command(...)`/`@<parent>.group(...)` of cli.py, with click's default name."""
    tree = ast.parse((PACKAGE / "cli.py").read_text(encoding="utf-8"))
    parents: dict[str, tuple[str, str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        for decorator in node.decorator_list:
            if not (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute)):
                continue
            if decorator.func.attr not in ("command", "group") or not isinstance(decorator.func.value, ast.Name):
                continue
            if decorator.func.value.id == "click":  # the root group (`main`)
                continue
            named = [arg.value for arg in decorator.args if isinstance(arg, ast.Constant)]
            named += [kw.value.value for kw in decorator.keywords if kw.arg == "name" and isinstance(kw.value, ast.Constant)]
            name = named[0] if named else node.name.replace("_", "-")
            parents[node.name] = (decorator.func.value.id, name)

    def path(function: str) -> str:
        parent, name = parents[function]
        return f"spec2viz {name}" if parent == "main" else f"{path(parent)} {name}"

    return {path(function) for function in parents}


def cli_commands() -> set[str]:
    return commands_from_click() or commands_from_source()


def package_modules() -> list[str]:
    return sorted(
        f"spec2viz/{sub}/{module.name}"
        for sub in SUBPACKAGES
        for module in (PACKAGE / sub).glob("*.py")
        if module.name != "__init__.py"
    )


def matrix_rows(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("| SV-")]


def test_cli_tree_is_read_from_spec2viz() -> None:
    commands = cli_commands()
    # the four subgroups of the help, so a parsing slip cannot pass the next test vacuously
    assert {"spec2viz diagram", "spec2viz catalog", "spec2viz notation", "spec2viz palette"} <= commands
    assert "spec2viz diagram from-graph" in commands


def test_every_cli_command_and_subgroup_has_a_row() -> None:
    rows = "\n".join(matrix_rows(MATRIX.read_text(encoding="utf-8")))
    missing = sorted(command for command in cli_commands() if f"`{command}`" not in rows)
    assert not missing, f"commands of the spec2viz help without a row in {MATRIX.name}: {missing}"


def test_every_compiler_renderer_linter_and_generator_module_has_a_row() -> None:
    modules = package_modules()
    assert modules, f"no modules under {PACKAGE}"
    rows = "\n".join(matrix_rows(MATRIX.read_text(encoding="utf-8")))
    missing = [module for module in modules if f"`{module}`" not in rows]
    assert not missing, f"spec2viz modules without a row in {MATRIX.name}: {missing}"


def test_every_spec2viz_test_file_maps_to_a_row() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    mapped = set(re.findall(r"^\| `(tests/test_[a-z0-9_]+\.py)` \| SV-", text, flags=re.MULTILINE))
    files = {f"tests/{path.name}" for path in (SPEC2VIZ / "tests").glob("test_*.py")}
    assert files, f"no tests under {SPEC2VIZ / 'tests'}"
    assert not sorted(files - mapped), f"spec2viz test files without a row: {sorted(files - mapped)}"


def test_every_row_has_exactly_one_mode_and_no_dismissal() -> None:
    rows = matrix_rows(MATRIX.read_text(encoding="utf-8"))
    assert rows
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert sum(cell in MODES for cell in cells) == 1, f"row without exactly one mode: {cells[0]}"
        lowered = row.lower()
        assert "descartad" not in lowered and "fuera de alcance" not in lowered, f"dismissed row: {cells[0]}"

FILE:instruccion
Cold-bundle de la tarea task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz aparecen en la matriz.
- Todos los módulos de compiladores, renderizadores, linters y generadores del paquete spec2viz aparecen en la matriz.
- Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada.
- Cada fila en modo reemplazar nombra el sustituto y la prueba que demostrará la equivalencia.
- Cada fila en modo usar sldb directamente cita la operación de la API pública de SLDB que la respalda, y no define ningún envoltorio en specIR.
- Cada fila en modo migrado a sldb cita la tarea de sldb que la migra (SpecSync, generador de spec desde grafo y AST, modelos de spec o emparejamiento de átomos) y las pruebas de spec2viz que se portan a sldb.
- Cada consumidor inventariado cita el archivo donde importa o invoca spec2viz.
- Existe un atom con la decisión sobre el YAML de spec frente al grafo, con las alternativas descartadas, la regla para diseño previo a la implementación y el destino de los specs existentes.
- El gate de retiro está escrito como lista comprobable: toda fila con su condición cumplida; la suite de spec2viz pasa contra specIR o tiene prueba equivalente declarada por fila reemplazada; ningún consumidor importa ni invoca spec2viz; ningún store registra modelos spec2viz.sldb_models.

