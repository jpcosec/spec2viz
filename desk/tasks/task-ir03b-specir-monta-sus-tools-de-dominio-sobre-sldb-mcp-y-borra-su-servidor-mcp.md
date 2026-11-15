---
sldb:
  by: agent
  at: '2026-11-15T21:18:56Z'
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
- Inventario de tests: los módulos de prueba test_dry_run, test_mutability, test_no_writes, test_read_tools, test_write_tools y el ayudante writing de la carpeta de pruebas MCP de specIR se borran porque las pruebas MCP de sldb tienen su equivalente (mismos nombres; writing en mcp_helpers y mcp_world). Lo que dependía del store real de IR y su federación (lectura del SpecDoc de spec2viz enlazado y no-escritura sobre deskops y spec2viz) pasa a tests/test_mcp_extension.py. tests/conftest.py y tests/models/blog.py levantan sldb mcp --extension specir.mcp_extension:register.
- Contexto y niveles: los de sldb mcp, sldb.mcp.context.ServerContext (store_path, project_root, level, actor, log) y los niveles 0 lectura, 1 contenido, 2 reglas como datos.
- Imports: la extensión es el único módulo de specIR que alcanza sldb.mcp (contrato de extensión: changes, paging, registry, write) y, a través de él, mcp; el resto de specIR solo usa sldb.api. tests/test_imports.py lo comprueba y que no quede servidor propio ni script specir-mcp.

Decisiones (bundle 1):
- Inventario de dominio: hoy solo claims_verified (IR05 D2-E); las tools de IR10 no existen y quedan fuera, IR10 las añadirá a esta misma extensión.
- "Si el store los registra" es sldb.api.is_model_registered; la forma de cada fila de specir_types es {type, layer, description, fields, registered, documents} y la página de sldb.mcp.paging; specir_nodes da {export_id, address, type, layer, title, path} más los campos de procedencia.
- La señal unknown_model sale por el canal de sldb: la respuesta lleva la marca signal con candidates = los tipos de dominio, el guard de sldb (settle) la registra en el log de señales del servidor (list_signals) y añade registered_as_signal y suggestions.
- Equivalencia de tests verificada contra sldb en de09290c (ce0a854e): los cinco test_*.py existen con el mismo nombre y los mismos casos (read_tools: el de federación spec2viz no tiene par y se porta a tests/test_mcp_extension.py); sldb no se edita.

## Validation

_List the checks required before this task can close._

- Una prueba de imports confirma que ningún módulo de specIR implementa el servidor MCP ni importa el paquete mcp salvo la extensión de dominio
- Un cliente MCP real por stdio contra sldb mcp --extension lista las tools de sldb y las de dominio de specIR
- Con nivel 0 las tools de escritura no existen y leer no cambia el árbol del store (comparación antes y después)
- Las pruebas de specIR que cubrían el servidor migrado se han portado a sldb o borrado con su código, y las restantes pasan

## Done When

_Name the observable condition that makes the task complete._

Un cliente MCP real por stdio contra sldb mcp con la extensión de specIR ve las tools de sldb y las de dominio, leer no escribe en el store, y el paquete specIR no contiene ya su servidor MCP propio ni importa mcp directamente.
