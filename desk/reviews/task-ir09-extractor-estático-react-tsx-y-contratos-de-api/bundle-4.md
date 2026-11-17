---
sldb:
  by: agent
  at: '2026-11-17T16:16:04Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir09-extractor-estático-react-tsx-y-contratos-de-api-bundle-4
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261117-161518/context-review/task-ir09-extractor-estático-react-tsx-y-contratos-de-api/bundle/778f5a6266d7570bf3c068cb8ccdf39c2ebca10a96293b1f12de519c90af6fff/attempt-2
input_sha256: 778f5a6266d7570bf3c068cb8ccdf39c2ebca10a96293b1f12de519c90af6fff
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ca19a7c39fe255665938cc8247f177171514444cb8ab5d9eff89e398dd684dae
output_sha256: 6b0e7c0b0d4394a263cb35a2e05ca5e8af5cbc95d0225cacdb8b74033166d6af
# pending | accepted | rejected | incomplete
verdict: accepted
reason: '1: manda la precisión (a): .tsx, .ts y .js obligatorios; la frase ''si el
  caso lo pide'' del Scope queda sustituida. 2: code_facts da para TS/JS facts de
  símbolo (función, componente, hook) con nombre, ruta, span y attrs.calls, como en
  Python (sldb/src/sldb/code/ts_calls.py: ''the calls a function, hook or component
  makes''); el emparejamiento es por el name canónico de la llamada contra el nombre
  del símbolo; si code_facts no da ese fact, EJECUTOR BLOQUEADO con la salida, hallazgo
  para sldb. 3: PublishButton y PublishAction son ejemplos; lo exigido son los tipos
  y las relaciones triggers e invokes hasta la ApiOperationDoc de publicar. 4: todos
  los espejos de depends_on están cerrados; 0590ed11 es el commit mínimo y ya contiene
  B2 y C1-C5.'
# ISO 8601 timestamp
created_at: '2026-11-17T16:15:45.777268+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T16:16:02.495381+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-ir09-extractor-estático-react-tsx-y-contratos-de-api

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-161518/context-review/task-ir09-extractor-estático-react-tsx-y-contratos-de-api/bundle/778f5a6266d7570bf3c068cb8ccdf39c2ebca10a96293b1f12de519c90af6fff/attempt-2.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: 1: manda la precisión (a): .tsx, .ts y .js obligatorios; la frase 'si el caso lo pide' del Scope queda sustituida. 2: code_facts da para TS/JS facts de símbolo (función, componente, hook) con nombre, ruta, span y attrs.calls, como en Python (sldb/src/sldb/code/ts_calls.py: 'the calls a function, hook or component makes'); el emparejamiento es por el name canónico de la llamada contra el nombre del símbolo; si code_facts no da ese fact, EJECUTOR BLOQUEADO con la salida, hallazgo para sldb. 3: PublishButton y PublishAction son ejemplos; lo exigido son los tipos y las relaciones triggers e invokes hasta la ApiOperationDoc de publicar. 4: todos los espejos de depends_on están cerrados; 0590ed11 es el commit mínimo y ya contiene B2 y C1-C5.
