FILE:desk/tasks/task-ir03b-specir-monta-sus-tools-de-dominio-sobre-sldb-mcp-y-borra-su-servidor-mcp.md
---
sldb:
  by: agent
  at: '2026-11-15T21:11:44Z'
  authority: generated
  via: save_document_payload
id: task-ir03b-specir-monta-sus-tools-de-dominio-sobre-sldb-mcp-y-borra-su-servidor-mcp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-espejo-sldb-sldb-mcp-servidor-mcp-genérico-a
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-depende-solo-de-la-api-pública-de-sldb
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
---

# IR03b specIR monta sus tools de dominio sobre sldb mcp y borra su servidor MCP

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: lo genérico va a sldb. El servidor MCP de IR03 e IR04 (niveles 0, 1 y 2, propose_changes y apply_changes) no tiene nada de specIR y se migra a sldb mcp, que trae el log de señales y un punto de extensión. specIR no puede conservar una copia.

## Goal

_Describe the concrete result this task must produce._

specIR deja su servidor MCP propio y monta sus tools de dominio sobre sldb mcp por el punto de extensión de sldb (build_server con extensions=[fn(server, ctx)] y la opción --extension modulo:funcion de sldb mcp); el código migrado a sldb se borra del paquete specIR.

## Scope

_State what is in scope and what is out of scope._

Dentro: una función de extensión en specIR que registra sus tools de dominio sobre el servidor de sldb mcp, con el mismo contexto y los mismos niveles; las tools de dominio que hoy viven en el paquete specir.mcp y no son genéricas (por ejemplo las de IR10 cuando existan) pasan a esa extensión; borrar el código migrado del paquete specIR: todo lo que hay bajo src/specir/mcp salvo lo de dominio, y los tests que se portaron a sldb; ajustar las pruebas de specIR para que levanten sldb mcp con --extension y las ejerzan con un cliente MCP real por stdio sobre una copia aislada del store. Fuera: reescribir el servidor genérico o su log de señales (son de sldb, tarea espejo A); tools de deshacer (IR04b); tools de impacto (IR10).

## Implementation Path

_Outline the expected implementation route or affected surface._

Esperar a que cierre la tarea espejo A (sldb mcp con punto de extensión). Luego mover lo de dominio a una función fn(server, ctx) del paquete specIR, probar el arranque con sldb mcp --store ... --level ... --extension specir.mcp_extension:register y borrar src/specir/mcp con git rm tras comprobar que cada módulo borrado tiene su equivalente en sldb. Sin copiar el servidor ni su log de señales.

Decisiones (preflight 1):
- Módulo y función de la extensión: specir.mcp_extension:register (src/specir/mcp_extension.py), firma register(server, context) del contrato sldb.mcp.extension.
- Frontera de borrado: src/specir/mcp se borra entero (paging, addresses, mutability, changes, read_tools, write_tools y server están en sldb/src/sldb/mcp desde ce0a854e). Lo único de dominio que había era claims_verified de write_tools (IR05 D2-E: un agente no escribe verificacion: verificado por el MCP), que sldb no migró a propósito; pasa a la extensión, que desde nivel 1 sirve propose_changes y apply_changes de un mismo WriteTools de sldb con esa comprobación delante de propose_changes. Tools de dominio nuevas y pequeñas sobre los tipos de IR06 (specir.models.domain), de solo lectura y en todos los niveles: specir_types (tipos de dominio, capa, campos propios, si el store los registra y cuántos documentos tiene) y specir_nodes (nodos de specIR del store con su procedencia, filtrables por tipo, capa, origen y verificación, paginados; un tipo desconocido es señal unknown_model).
- Inventario de tests: tests/mcp/test_dry_run.py, test_mutability.py, test_no_writes.py, test_read_tools.py, test_write_tools.py y writing.py se borran porque sldb/tests/mcp tiene su equivalente (mismos nombres; writing.py en mcp_helpers.py y mcp_world.py). Lo que dependía del store real de IR y su federación (lectura del SpecDoc de spec2viz enlazado y no-escritura sobre deskops y spec2viz) pasa a tests/test_mcp_extension.py. tests/conftest.py y tests/models/blog.py levantan sldb mcp --extension specir.mcp_extension:register.
- Contexto y niveles: los de sldb mcp, sldb.mcp.context.ServerContext (store_path, project_root, level, actor, log) y los niveles 0 lectura, 1 contenido, 2 reglas como datos.
- Imports: la extensión es el único módulo de specIR que alcanza sldb.mcp (contrato de extensión: changes, paging, registry, write) y, a través de él, mcp; el resto de specIR solo usa sldb.api. tests/test_imports.py lo comprueba y que no quede servidor propio ni script specir-mcp.

## Validation

_List the checks required before this task can close._

- Una prueba de imports confirma que ningún módulo de specIR implementa el servidor MCP ni importa el paquete mcp salvo la extensión de dominio
- Un cliente MCP real por stdio contra sldb mcp --extension lista las tools de sldb y las de dominio de specIR
- Con nivel 0 las tools de escritura no existen y leer no cambia el árbol del store (comparación antes y después)
- Las pruebas de specIR que cubrían el servidor migrado se han portado a sldb o borrado con su código, y las restantes pasan

## Done When

_Name the observable condition that makes the task complete._

Un cliente MCP real por stdio contra sldb mcp con la extensión de specIR ve las tools de sldb y las de dominio, leer no escribe en el store, y el paquete specIR no contiene ya su servidor MCP propio ni importa mcp directamente.

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

FILE:desk/atoms/atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir.md
---
sldb:
  by: agent
  at: '2026-11-15T05:05:58Z'
  authority: generated
  via: save_document_payload
id: atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
title: Principios de seguridad de la superficie MCP de specIR
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- topic:procedencia
- layer:superficie
provenance: fundamentos_modelado_semantico_mcp.md
---

# Principios de seguridad de la superficie MCP de specIR

## Answer

La superficie MCP sigue estos principios: las consultas no tienen efectos laterales; proponer, validar y aplicar una modificación son pasos separados; no se aplica un cambio sobre un estado que ya no es el que se validó; cada nodo y relación declara su procedencia y una inferencia de un LLM nunca pasa a hecho validado en silencio; los límites de escritura los impone el servidor, no el agente ni la interfaz; el sistema conserva lo que desconoce en vez de rellenarlo. Mecanismos decididos (docs/decisiones/contrato-de-escritura-mcp.md, 2026-11-15): la propuesta es un lote efímero prevalidado que se aplica todo o nada con sldb.api.apply_batch (atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado); la aplicación se protege con guardas expected_source_hash por documento y, en nivel 2, con store_hash atómico (atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2); el nivel de escritura se fija al arrancar el servidor, 0 por defecto (atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor); deshacer es un lote inverso con guardas (atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas). Procedencia decidida (docs/decisiones/procedencia-y-divergencia.md, 2026-11-15): ejes origen y verificacion con la autoridad de SLDB por tabla (atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla); lo desconocido se nombra y el MCP nunca escribe verificado (atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica); anclas de SLDB y divergencia según el origen (atom-un-nodo-extraído-se-ancla-con-sldb-y-la-divergencia-con-el-código-se-calcula-según-su-origen).

FILE:instruccion
Cold-bundle de la tarea task-ir03b-specir-monta-sus-tools-de-dominio-sobre-sldb-mcp-y-borra-su-servidor-mcp: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Una prueba de imports confirma que ningún módulo de specIR implementa el servidor MCP ni importa el paquete mcp salvo la extensión de dominio
- Un cliente MCP real por stdio contra sldb mcp --extension lista las tools de sldb y las de dominio de specIR
- Con nivel 0 las tools de escritura no existen y leer no cambia el árbol del store (comparación antes y después)
- Las pruebas de specIR que cubrían el servidor migrado se han portado a sldb o borrado con su código, y las restantes pasan

