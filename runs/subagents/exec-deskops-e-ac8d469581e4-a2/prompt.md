Task: task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import
Title: IR04b, cierre: la prueba de identidad tras deshacer compara también el store por contenido, y no importa módulos internos de sldb
Status: active
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-21T00:25:44Z'
  authority: generated
  via: save_document_payload
id: task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-da81f2bd34e0 FALLA sobre 33846f5: tests/test_mcp_undo.py::test_a_stale_batch_is_refused_without_writing_and_undone_once_the_foreign_change_is_reverted
  falla en ''assert content() == mds'' (línea 208). La causa no es el deshacer: content()
  lista el store con sldb.api.load_runtime_documents, que omite en silencio los modelos
  que no resuelven (los heredados de deskops, model_ref deskops.models...), así que
  al empezar ve 53 documentos y después de una escritura en el mismo proceso ve 506.
  Intento 2, como dice la resolución aceptada: enumerar con sldb.api.select_documents
  (filas export_id, model, name, path, que no dependen de importar modelos) y comparar
  cada documento por el sha256 del texto de su archivo sin el bloque sldb (el md_digest
  local ya existente). Que el conjunto de claves sea estable entre las dos instantáneas.
  Si hace falta, que content() del test stale compare solo los .md y deje la comparación
  del store al test de identidad. Los cuatro archivos de tests tienen que pasar, de
  a uno. Commit desde tu worktree con ''git commit -- <rutas>'' y trailer Task-Id.'
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

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-ir04b-cierre-la-prueba-de-identidad-tras-deshacer-compara-tambien-el-store-por-contenido-y-no-import"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-ac8d469581e4-a2`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-ac8d469581e4-a2

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
