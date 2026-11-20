---
sldb:
  by: agent
  at: '2026-11-20T21:13:59Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir09-extractor-estático-react-tsx-y-contratos-de-api-preflight-4
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir09-extractor-estático-react-tsx-y-contratos-de-api@sha256:c0f15ef03296498a6f45f32676589ba9a737ac6224db6404c3bfc2063b999cfc
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-211322/context-review/task-ir09-extractor-estático-react-tsx-y-contratos-de-api/preflight/2d173ddfa4ca1828b0adf954a05c086791848217ed51e5dd70a5d8cc8ba7adc2/attempt-1
input_sha256: 2d173ddfa4ca1828b0adf954a05c086791848217ed51e5dd70a5d8cc8ba7adc2
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 74028ad97e66646a9f774bfd0bc585ce2babbfcb1ff3b3ee072ac721cddf6d8d
output_sha256: 83e5664e734d74ad8df80593dac30f0ce6763805c852cfbcf0801507d0a3bf48
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. 1) Mandan las Precisiones (a), que
  son posteriores al Scope: el fixture tests/fixtures/blog_frontend tiene que traer
  al menos un .tsx, un .ts y un .js, los tres. Si falta alguno, el ejecutor lo agrega
  al fixture. La frase del Scope (''si el caso lo pide'') queda superada. 2) Los nombres
  no son normativos: la prueba compara tipos y relaciones con tests/models/blog.py,
  como dice (a). PublishButton y PublishAction son los nombres esperados del fixture
  y se mencionan como ejemplo. 3) Cardinalidad: un InterfaceActionDoc por función
  handler, aunque la compartan varios controles; cada control tiene su triggers hacia
  esa misma acción. Una acción tiene un invokes por cada llamada HTTP literal que
  resuelve a una ApiOperationDoc, así que pueden ser varios. 4) Si la función handler
  (siguiendo un nivel por nombre canónico) contiene varias llamadas HTTP, cada una
  se evalúa sola: las literales que resuelven dan un invokes cada una, y las demás
  van a not_derived con su motivo. 5) De plan.py y write.py solo se puede agregar
  lo que el frontend necesite sin cambiar el comportamiento de IR08: funciones nuevas
  o parámetros opcionales con default igual al de hoy. not_derived es la lista de
  strings de ExtractionReport (src/specir/extract/write.py:33), con un motivo legible
  por entrada, como en IR08. Normalización de URL: se compara el path de la URL literal
  (sin esquema, host ni query) con el path de la ApiOperationDoc; un segmento de parámetro
  de la operación ({id}, <int:pk> o el formato que IR08 haya escrito) casa con cualquier
  segmento no vacío, y la barra final se ignora. El commit lleva el trailer ''Task-Id:
  task-ir09-extractor-estático-react-tsx-y-contratos-de-api'' con ''git commit --
  <rutas>''.'
# ISO 8601 timestamp
created_at: '2026-11-20T21:13:36.403614+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T21:13:57.633708+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-ir09-extractor-estático-react-tsx-y-contratos-de-api

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-211322/context-review/task-ir09-extractor-estático-react-tsx-y-contratos-de-api/preflight/2d173ddfa4ca1828b0adf954a05c086791848217ed51e5dd70a5d8cc8ba7adc2/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1) Mandan las Precisiones (a), que son posteriores al Scope: el fixture tests/fixtures/blog_frontend tiene que traer al menos un .tsx, un .ts y un .js, los tres. Si falta alguno, el ejecutor lo agrega al fixture. La frase del Scope ('si el caso lo pide') queda superada. 2) Los nombres no son normativos: la prueba compara tipos y relaciones con tests/models/blog.py, como dice (a). PublishButton y PublishAction son los nombres esperados del fixture y se mencionan como ejemplo. 3) Cardinalidad: un InterfaceActionDoc por función handler, aunque la compartan varios controles; cada control tiene su triggers hacia esa misma acción. Una acción tiene un invokes por cada llamada HTTP literal que resuelve a una ApiOperationDoc, así que pueden ser varios. 4) Si la función handler (siguiendo un nivel por nombre canónico) contiene varias llamadas HTTP, cada una se evalúa sola: las literales que resuelven dan un invokes cada una, y las demás van a not_derived con su motivo. 5) De plan.py y write.py solo se puede agregar lo que el frontend necesite sin cambiar el comportamiento de IR08: funciones nuevas o parámetros opcionales con default igual al de hoy. not_derived es la lista de strings de ExtractionReport (src/specir/extract/write.py:33), con un motivo legible por entrada, como en IR08. Normalización de URL: se compara el path de la URL literal (sin esquema, host ni query) con el path de la ApiOperationDoc; un segmento de parámetro de la operación ({id}, <int:pk> o el formato que IR08 haya escrito) casa con cualquier segmento no vacío, y la barra final se ignora. El commit lleva el trailer 'Task-Id: task-ir09-extractor-estático-react-tsx-y-contratos-de-api' con 'git commit -- <rutas>'.
