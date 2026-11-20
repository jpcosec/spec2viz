---
sldb:
  by: agent
  at: '2026-11-20T22:39:09Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz-bundle-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz@sha256:1bd89425357501cf6a57cb356675ed117b7d25efe209084404cf718a5079310a
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-223808/context-review/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz/bundle/88dd62010b545751f1a590077f1c7d312fca4b5fd06cffcbdeb387678a86d8d3/attempt-1
input_sha256: 88dd62010b545751f1a590077f1c7d312fca4b5fd06cffcbdeb387678a86d8d3
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 1460d0ffeb57c8e45125a142b6377e999b648587b83f3ce946719fd489b47a84
output_sha256: 26fe80a8dfbf97b34467a6fa2548a2c7ba9472301061a426246591182af583df
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. Preflight 1) Los modos están en docs/spec2viz/matriz-de-cobertura.md,
  sección ''## Modos'' (línea 26: portar, reemplazar, usar sldb directamente y los
  demás de esa tabla, cada uno con su evidencia exigida). Las condiciones de retiro
  están en docs/spec2viz/gate-de-retiro.md. Una fila ''en modo reemplazar'' es una
  fila de la matriz con ese modo, y cuenta como cumplida cuando trae el sustituto
  y la prueba de equivalencia que pide la tabla de modos. 2) G1 a G7 son las condiciones
  del gate, definidas en docs/spec2viz/gate-de-retiro.md, con su estado actual en
  la tabla de docs/spec2viz/acta-de-retiro.md (líneas 103 a 109). El comprobador lee
  ese estado y no lo inventa. 3) IR13c se retiró: manda la precisión 1 de la tarea
  (''IR13c se retiró, sus filas pasaron a usar sldb directamente; no bloquea''). La
  mención en ''Fuera'' es histórica y no hay que tocar nada de IR13c. 4) Las cifras
  de los bloques ''Estado (...)'' de la tarea son fotos históricas, no requisitos.
  Lo vigente es lo que el comprobador recalcula sobre la matriz y el inventario actuales,
  y el acta se actualiza con eso. Bundle 1) Reciben pedido de migración los desks
  de los consumidores del inventario que tienen desk registrado (deskops repo list):
  graph_ui, deskops, sldb y pron. Se envía con deskops message send --to <repo> --kind
  suggestion, nombrando cada dependencia (archivo:línea). spec2viz no recibe, porque
  es el que se retira, ni IR, que es este repo y migra en esta tarea. Un consumidor
  del inventario sin desk registrado figura en el acta con ''sin desk: pedido a JP''.
  2) Un SKILL.md, agents.md o archivo de habilidad cuenta como dependencia operativa
  si manda a correr spec2viz (una línea de comando o un bloque de código que lo invoca,
  como detecta la precisión 3). Una mención en prosa sin instrucción de ejecutarlo
  es documentación y no cuenta. 3) En el acta, la fila de IR dice ''propio: migrado
  en esta tarea'' con el commit, y la del store spec2viz/.sldb dice ''G5: decidido,
  se ejecuta en IR'' con su referencia, sin mensaje. El commit lleva ''git commit
  -- <rutas>'' y el trailer ''Task-Id: task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz''.'
# ISO 8601 timestamp
created_at: '2026-11-20T22:38:23.101864+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T22:39:07.713479+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-223808/context-review/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz/bundle/88dd62010b545751f1a590077f1c7d312fca4b5fd06cffcbdeb387678a86d8d3/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. Preflight 1) Los modos están en docs/spec2viz/matriz-de-cobertura.md, sección '## Modos' (línea 26: portar, reemplazar, usar sldb directamente y los demás de esa tabla, cada uno con su evidencia exigida). Las condiciones de retiro están en docs/spec2viz/gate-de-retiro.md. Una fila 'en modo reemplazar' es una fila de la matriz con ese modo, y cuenta como cumplida cuando trae el sustituto y la prueba de equivalencia que pide la tabla de modos. 2) G1 a G7 son las condiciones del gate, definidas en docs/spec2viz/gate-de-retiro.md, con su estado actual en la tabla de docs/spec2viz/acta-de-retiro.md (líneas 103 a 109). El comprobador lee ese estado y no lo inventa. 3) IR13c se retiró: manda la precisión 1 de la tarea ('IR13c se retiró, sus filas pasaron a usar sldb directamente; no bloquea'). La mención en 'Fuera' es histórica y no hay que tocar nada de IR13c. 4) Las cifras de los bloques 'Estado (...)' de la tarea son fotos históricas, no requisitos. Lo vigente es lo que el comprobador recalcula sobre la matriz y el inventario actuales, y el acta se actualiza con eso. Bundle 1) Reciben pedido de migración los desks de los consumidores del inventario que tienen desk registrado (deskops repo list): graph_ui, deskops, sldb y pron. Se envía con deskops message send --to <repo> --kind suggestion, nombrando cada dependencia (archivo:línea). spec2viz no recibe, porque es el que se retira, ni IR, que es este repo y migra en esta tarea. Un consumidor del inventario sin desk registrado figura en el acta con 'sin desk: pedido a JP'. 2) Un SKILL.md, agents.md o archivo de habilidad cuenta como dependencia operativa si manda a correr spec2viz (una línea de comando o un bloque de código que lo invoca, como detecta la precisión 3). Una mención en prosa sin instrucción de ejecutarlo es documentación y no cuenta. 3) En el acta, la fila de IR dice 'propio: migrado en esta tarea' con el commit, y la del store spec2viz/.sldb dice 'G5: decidido, se ejecuta en IR' con su referencia, sin mensaje. El commit lleva 'git commit -- <rutas>' y el trailer 'Task-Id: task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz'.
