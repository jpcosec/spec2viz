---
sldb:
  by: agent
  at: '2026-11-20T23:47:06Z'
  authority: generated
  via: create_document
id: task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR04b, cierre: la prueba de identidad tras deshacer compara también el store por contenido, y no importa módulos internos de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

IR04b (código 1be6fc1 y 57616e8) agotó sus dos intentos. El deshacer por MCP funciona y las pruebas pedidas pasan, pero el tester del intento 2 (runs/subagents/exec-deskops-t-ef3b25a2dd59-a2-testing) marcó dos cosas. (1) La Validación 1, fijada por el coordinador según el contrato de sldb 'mismo contenido salvo procedencia' (nota 20261118-211934), pide comparar el sha256 del texto sin bloque sldb igual antes y después, documento por documento y el store por el mismo criterio; la prueba compara los .md pero no el store. (2) md_digest en tests importa strip_block de sldb.models.provenance_block, un módulo interno, contra el pill pill-guardrail-specir-solo-usa-la-api-pública-de-sldb, que aplica también a tests/.

## Goal

_Describe the concrete result this task must produce._

En tests/test_mcp_undo.py la prueba de identidad compara, además de cada .md, el estado del store antes y después de deshacer por el mismo criterio de contenido: para cada documento trackeado, su payload o el content hash que exponga sldb.api. Pasa sin xfail. Y el digest de contenido de las pruebas usa solo la API pública de sldb (sldb.api; por ejemplo la función de sldb/api/documents/content_hash.py si se exporta, o el payload por sldb.api), sin importar sldb.models ni otros módulos internos.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/test_mcp_undo.py y el helper de digest que use. Fuera: el código de deshacer de src/specir/mcp_extension.py, salvo que la comparación del store revele un fallo real; en ese caso el ejecutor lo informa y lo arregla dentro del alcance de IR04b.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: leer tests/test_mcp_undo.py y la prueba de identidad. p2: agregar la comparación del store (lista de documentos trackeados con su contenido o content hash por sldb.api) antes y después. p3: reemplazar el import interno por la API pública. p4: correr tests/test_mcp_undo.py, tests/models/test_blog_chain.py, tests/models/test_domain_tools.py y tests/test_mcp_extension.py, de a uno, en verde. p5: commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_mcp_undo.py

## Done When

_Name the observable condition that makes the task complete._

Los cuatro archivos de tests pasan; la prueba de identidad compara .md y store por contenido; no hay imports de módulos internos de sldb en tests/test_mcp_undo.py.
