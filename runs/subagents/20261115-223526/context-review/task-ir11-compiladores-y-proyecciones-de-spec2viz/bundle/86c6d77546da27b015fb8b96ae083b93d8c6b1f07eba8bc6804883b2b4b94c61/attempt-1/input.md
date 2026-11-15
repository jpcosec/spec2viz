FILE:desk/tasks/task-ir11-compiladores-y-proyecciones-de-spec2viz.md
---
sldb:
  by: agent
  at: '2026-11-15T22:34:04Z'
  authority: generated
  via: save_document_payload
id: task-ir11-compiladores-y-proyecciones-de-spec2viz
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
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-espejo-sldb-modelos-de-spec-por-tipo-de-diagrama-d3
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
from_drawer: desk/drawer/tasks/task-ir11-compiladores-y-proyecciones-de-spec2viz.md
---

# IR11 Compiladores y proyecciones de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Los compiladores son el centro de spec2viz: convierten un spec en una representación lista para dibujar. Sin cubrirlos, ninguna otra parte de la capa visual puede migrar, y es donde se aplica la decisión sobre el YAML de spec frente al grafo.

## Goal

_Describe the concrete result this task must produce._

specIR compila todos los tipos de diagrama que compila spec2viz y produce diagramas tanto desde un spec autorado como desde una proyección del grafo, según el contrato decidido en la tarea de cobertura.

## Scope

_State what is in scope and what is out of scope._

Dentro: los modelos de spec, su carga y su validación para clase, secuencia, estado, componente, actividad, despliegue, matriz y reflexión se toman de sldb (D3, tarea espejo de sldb) y no se redefinen en specIR; representación intermedia visual propia de specIR y un compilador por tipo; materialización de proyecciones: de un ViewDoc evaluado por la API de SLDB sobre su grafo y de un SpecDoc con sus SpecNodeDoc a la misma representación intermedia. specIR puede transformar esos resultados en nodos y aristas específicos del dominio/diagrama, pero la consulta del store, el índice, las aristas autoradas y los recorridos genéricos siguen siendo de SLDB y se consumen mediante su API pública. Los modelos de vocabulario visual se usan desde SLDB y no se redefinen. Fuera: índice o backend genérico de grafo, renderizado a formatos de salida, linter y recursos empaquetados; sincronización al store, catálogos y consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Los modelos de spec, su carga y su validación vienen de sldb (D3): specIR los importa de su API pública y no define ninguno; los compiladores y las proyecciones consumen esos modelos. Módulos de compilación en el paquete specIR; resolución de vistas por la API pública de SLDB. Paridad: los fixtures y pruebas de compiladores de spec2viz se portan a tests/visual/ de specIR y se comparan por equivalencia estructural normalizada de la representación intermedia: mismos tipos de elemento, mismos campos con los mismos valores, mismos nodos y aristas con los mismos extremos y atributos, comparados tras ordenar de forma determinista las colecciones cuyo orden no es significativo (nodos y aristas por id) y conservando el orden donde sí lo es (pasos de actividad, mensajes de secuencia, miembros de clase). Solo se excluye de la comparación la metadata de procedencia (origen, marcas de tiempo, rutas absolutas); cualquier otra diferencia es un fallo o una diferencia declarada en la matriz. El código de specIR bajo src/ no importa spec2viz. Las pruebas de paridad bajo tests/ sí pueden importar spec2viz como oráculo de desarrollo para producir el valor esperado, marcadas como pruebas de paridad y omitidas si spec2viz no está instalado; cuando spec2viz se retire, el oráculo se sustituye por los resultados guardados de su última ejecución. Propiedad de archivos compartidos: esta tarea crea src/specir/visual/__init__.py con las exportaciones de modelos de spec, compiladores y proyecciones; la tarea IR13d lo extiende después con la API pública completa, y corre siempre después de esta porque depende de ella por la cadena IR13a e IR12. `projections.py` obtiene datos del store mediante la API pública de SLDB: `run_view` para ViewDoc compuesto, `evaluate_projection_view` para ViewDoc de proyección y `resolve_view` para SpecDoc; luego los transforma a la representación visual específica. No consulta archivos/índices internos ni reproduce recorridos genéricos.

Precisiones (preflight): el contrato es el de la tarea de cobertura (IR07): filas SV-B01 a SV-B10 y SV-A14 de docs/spec2viz/matriz-de-cobertura.md (modo migrar tal cual) y la propuesta docs/decisiones/fuente-de-verdad-del-diagrama.md (pendiente de JP; no cambia IR11: spec autorado y proyección compilan a la misma representación intermedia). Oráculo: spec2viz en la revisión 2de1056, instalado editable en .venv; el corpus son los 44 specs de spec2viz (tests/fixtures con invalid/, examples/, docs/architecture/spec2viz/) copiados a tests/visual/fixtures/spec2viz/, y los resultados guardados de su última ejecución van en tests/visual/goldens/spec2viz-2de1056.json (tests/visual/parity.py los regenera). Errores tipados: misma clase y mismo texto al cargar y validar con sldb.api.notations.load_spec/validate_spec que con spec2viz, sobre ese corpus. Blog: el de IR06 (tests/models/blog.py y tests/fixtures/blog_chain.yaml); Post es DomainEntityDoc:post y las proyecciones son ViewDoc:post-states y ViewDoc:publish-components. Firmas de sldb 641ecdfa: sldb.api.run_view(store, name, params), sldb.api.notations.evaluate_projection_view(store, view_or_ref, pythonpath) y resolve_view(store, spec_ref, pythonpath).
 Carencia de sldb (pedida a su desk el 2026-11-15): sldb.api.notations exporta load_spec y validate_spec pero no las clases de los modelos de spec; hasta que las exporte, un único módulo de specIR (src/specir/visual/spec_models.py) las importa de sldb.models.notation.diagram_specs, con una excepción acotada a ese módulo en tests/test_imports.py; ningún otro módulo alcanza internos de sldb.

## Validation

_List the checks required before this task can close._

- Los ocho tipos de diagrama compilan en specIR, y cada fixture de compilador de spec2viz produce en specIR una representación intermedia estructuralmente equivalente a la de spec2viz según la normalización definida en el camino de implementación, o la diferencia está declarada en la fila correspondiente de la matriz de cobertura con su prueba equivalente.
- La función de normalización tiene su propia prueba: dos representaciones que difieren solo en el orden de nodos o en metadata de procedencia resultan iguales, y dos que difieren en un campo, un nodo o una arista resultan distintas.
- Los specs YAML existentes validan en specIR con los mismos errores tipados que en spec2viz, salvo que la decisión de la tarea de cobertura diga otra cosa.
- Un diagrama de componentes y uno de estados generados desde proyecciones del grafo del blog muestran la entidad Post y el store sigue teniendo un solo documento para ella.
- Compilar desde un spec autorado y desde la proyección equivalente del grafo da representaciones intermedias estructuralmente equivalentes según la misma normalización.
- specIR no define ninguna clase con el nombre de un modelo de vocabulario visual de SLDB.
- Ningún módulo bajo src/specir/ importa spec2viz (prueba de imports); spec2viz solo aparece importado en pruebas de paridad bajo tests/.
- specIR no define ninguna clase de modelo de spec por tipo de diagrama: los ocho se importan de sldb (prueba de imports y de nombres).

## Done When

_Name the observable condition that makes the task complete._

Las pruebas de paridad de compiladores pasan en specIR y las filas de compiladores y proyecciones de la matriz de cobertura tienen su condición de retiro cumplida.

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
Cold-bundle de la tarea task-ir11-compiladores-y-proyecciones-de-spec2viz: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Los ocho tipos de diagrama compilan en specIR, y cada fixture de compilador de spec2viz produce en specIR una representación intermedia estructuralmente equivalente a la de spec2viz según la normalización definida en el camino de implementación, o la diferencia está declarada en la fila correspondiente de la matriz de cobertura con su prueba equivalente.
- La función de normalización tiene su propia prueba: dos representaciones que difieren solo en el orden de nodos o en metadata de procedencia resultan iguales, y dos que difieren en un campo, un nodo o una arista resultan distintas.
- Los specs YAML existentes validan en specIR con los mismos errores tipados que en spec2viz, salvo que la decisión de la tarea de cobertura diga otra cosa.
- Un diagrama de componentes y uno de estados generados desde proyecciones del grafo del blog muestran la entidad Post y el store sigue teniendo un solo documento para ella.
- Compilar desde un spec autorado y desde la proyección equivalente del grafo da representaciones intermedias estructuralmente equivalentes según la misma normalización.
- specIR no define ninguna clase con el nombre de un modelo de vocabulario visual de SLDB.
- Ningún módulo bajo src/specir/ importa spec2viz (prueba de imports); spec2viz solo aparece importado en pruebas de paridad bajo tests/.
- specIR no define ninguna clase de modelo de spec por tipo de diagrama: los ocho se importan de sldb (prueba de imports y de nombres).

