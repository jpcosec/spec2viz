Task: task-ir10-reglas-semánticas-y-análisis-de-impacto
Title: IR10 Reglas semánticas y análisis de impacto
Status: draft
Current node: ritual-execution
Task type: task.code
From drawer: desk/drawer/tasks/task-ir10-reglas-semanticas-y-analisis-de-impacto.md
Effective pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
Effective atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-16T05:05:35Z'
  authority: generated
  via: save_document_payload
id: task-ir10-reglas-semánticas-y-análisis-de-impacto
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:impacto
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog
- task-ir08-extractor-estático-django-drf-y-sql
- task-ir09-extractor-estático-react-tsx-y-contratos-de-api
- task-espejo-sldb-graph-path-y-graph-paths-explicados-b3
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código
- atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir10-reglas-semanticas-y-analisis-de-impacto.md
---

# IR10 Reglas semánticas y análisis de impacto

## Rationale

_Explain why this task exists or the business driver behind it._

Tener el grafo no basta: el agente necesita que el sistema le diga qué se rompe cuando cambia un campo, un endpoint o una regla, y con qué evidencia. Es el criterio de éxito 4 de los fundamentos.

## Goal

_Describe the concrete result this task must produce._

Un conjunto de reglas RuleDoc de dominio que detectan brechas entre capas, evaluadas con el motor de reglas de sldb, y un análisis de impacto que usa los caminos explicados de sldb (graph_path y graph_paths, tarea espejo B3) y lo expone como tool de dominio sobre sldb mcp, con el camino que justifica cada afectado.

## Scope

_State what is in scope and what is out of scope._

Dentro: reglas RuleDoc, distribuidas por specIR como documentos, para cadenas rotas interfaz, API, operación, datos: acción sin operación de API, campo de interfaz ausente del serializer, operación sin handler, entidad sin persistencia, política sin representación en la interfaz; cada hallazgo con severidad, regla que lo produce y evidencia; operación de impacto de dominio: dado un nodo (campo, endpoint, regla, tabla), los nodos afectados en las demás capas, obtenidos con los caminos explicados de sldb, con la procedencia de cada tramo; tool de solo lectura para ambas, registrada como extensión de sldb mcp. Fuera: recorrer el grafo o explicar caminos en specIR (es de sldb, B3); proponer parches o cambios de código; aplicar correcciones al grafo; reglas que requieran ejecutar la aplicación.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las reglas se escriben en el lenguaje de reglas de sldb y se evalúan con sus operaciones públicas de reglas; el impacto llama a graph_path y graph_paths de sldb y solo añade el mapeo de dominio (qué tipos cuentan como afectados y cómo se nombran). La tool se registra como extensión de sldb mcp. Si el lenguaje de reglas o el recorrido no alcanzan para alguna brecha, la carencia se resuelve en sldb, no con lógica paralela en specIR. Depende de la tarea espejo B3.

## Validation

_List the checks required before this task can close._

- Por cada regla hay un store de prueba con la brecha sembrada y la evaluación la reporta con su severidad, la regla y los documentos implicados.
- Sobre el grafo completo del blog sin brechas sembradas, las reglas no reportan hallazgos.
- Dado el campo status de la tabla de posts, la operación de impacto devuelve PublishButton entre los afectados, con el camino completo de relaciones.
- Cada tramo del camino devuelto lleva su procedencia, y un camino que pasa por una relación inferida se señala como tal.
- Las tools de reglas e impacto no escriben en el store (comparación del árbol antes y después).
- Ninguna respuesta incluye un parche ni una modificación propuesta.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan, un agente puede responder por sldb mcp qué partes de la interfaz afecta un cambio en un campo, un endpoint o una regla del blog, y specIR no contiene ningún recorrido de grafo propio.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-ir10-reglas-semánticas-y-análisis-de-impacto"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-8ec8764345d1`:

    /mnt/ssd/proyectos/SLDB_1/IR/.worktrees/deskops-e-8ec8764345d1

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/IR. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/IR`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
