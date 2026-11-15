---
sldb:
  by: agent
  at: '2026-11-15T16:55:51Z'
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

Esperar a que cierre la tarea espejo A (sldb mcp con punto de extensión). Luego mover lo de dominio a una función fn(server, ctx) del paquete specIR, probar el arranque con sldb mcp --store ... --level ... --extension specir.mcp_extension:register (el nombre del módulo lo fija la tarea al implementarla) y borrar src/specir/mcp con git rm tras comprobar que cada módulo borrado tiene su equivalente en sldb. Sin copiar el servidor ni su log de señales.

## Validation

_List the checks required before this task can close._

- Una prueba de imports confirma que ningún módulo de specIR implementa el servidor MCP ni importa el paquete mcp salvo la extensión de dominio
- Un cliente MCP real por stdio contra sldb mcp --extension lista las tools de sldb y las de dominio de specIR
- Con nivel 0 las tools de escritura no existen y leer no cambia el árbol del store (comparación antes y después)
- Las pruebas de specIR que cubrían el servidor migrado se han portado a sldb o borrado con su código, y las restantes pasan

## Done When

_Name the observable condition that makes the task complete._

Un cliente MCP real por stdio contra sldb mcp con la extensión de specIR ve las tools de sldb y las de dominio, leer no escribe en el store, y el paquete specIR no contiene ya su servidor MCP propio ni importa mcp directamente.
