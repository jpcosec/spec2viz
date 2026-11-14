FILE:desk/tasks/task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro.md
---
sldb:
  by: agent
  at: '2026-11-12T01:31:27Z'
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
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
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

Dentro, una fila por cada capacidad de spec2viz, cada una con modo (migrar tal cual; reemplazar por otra arquitectura o experiencia con resultado equivalente; exponer desde specIR lo que ya vive en SLDB) y condición verificable de retiro:
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

## Validation

_List the checks required before this task can close._

- Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz aparecen en la matriz.
- Todos los módulos de compiladores, renderizadores, linters y generadores del paquete spec2viz aparecen en la matriz.
- Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada.
- Cada fila en modo reemplazar nombra el sustituto y la prueba que demostrará la equivalencia.
- Cada fila en modo exponer desde SLDB cita la operación de la API pública de SLDB que la respalda.
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

FILE:instruccion
Cold-bundle de la tarea task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz aparecen en la matriz.
- Todos los módulos de compiladores, renderizadores, linters y generadores del paquete spec2viz aparecen en la matriz.
- Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada.
- Cada fila en modo reemplazar nombra el sustituto y la prueba que demostrará la equivalencia.
- Cada fila en modo exponer desde SLDB cita la operación de la API pública de SLDB que la respalda.
- Cada consumidor inventariado cita el archivo donde importa o invoca spec2viz.
- Existe un atom con la decisión sobre el YAML de spec frente al grafo, con las alternativas descartadas, la regla para diseño previo a la implementación y el destino de los specs existentes.
- El gate de retiro está escrito como lista comprobable: toda fila con su condición cumplida; la suite de spec2viz pasa contra specIR o tiene prueba equivalente declarada por fila reemplazada; ningún consumidor importa ni invoca spec2viz; ningún store registra modelos spec2viz.sldb_models.

