---
sldb:
  by: agent
  at: '2026-11-17T11:19:56Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir08-extractor-estático-django-drf-y-sql-bundle-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir08-extractor-estático-django-drf-y-sql@sha256:714ea9a93fbd78049b742685bc2c0d2cd16c5d16a6a6b3d42cfb03768b60526b
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-111910/context-review/task-ir08-extractor-estático-django-drf-y-sql/bundle/b131b8dba009c32bd4a243d69456735a4392be18f94b1296bad0f9dd480d4823/attempt-1
input_sha256: b131b8dba009c32bd4a243d69456735a4392be18f94b1296bad0f9dd480d4823
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 1d9e9a5ef0be3594cf9e1ae86654ef8ed1d724b1ed4519db0a546ef36838341f
output_sha256: 9c0426622edb2b80260329dadc07045b9b561239de63e08209217c51362d3b51
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Adjudicado: (1) el informe es el valor que devuelve la función pública de
  specir.extract (listas creados, sin cambios, cambiados y no derivados), sin CLI
  ni otro canal; (2) apply_batch de sldb valida RelationTypeDoc al escribir, y los
  RuleDoc se comprueban con sldb rules check --store .sldb --format json como en rules_findings
  de tests/models/test_blog_chain.py; cualquier hallazgo de nivel error hace fallar
  la prueba; (3) pruebas nuevas en tests/extract/, organización libre; (4) golden
  = los nodos y relaciones de backend y datos de tests/models/blog.py (ApiOperationDoc,
  HandlerDoc, DomainOperationDoc, PolicyDoc, StateDoc, DomainEntityDoc y TableDoc
  con handled_by, executes, governed_by, writes y persisted_in; transitions si hay
  fact), mismos tipos y relaciones, títulos libres salvo la ruta POST /posts/{id}/publish
  y la tabla posts; InterfaceControlDoc e InterfaceActionDoc son de IR09; (5) todas
  las anclas se comprueban antes de apply_batch: si una no coincide, ValueError con
  el ref y no se escribe nada'
# ISO 8601 timestamp
created_at: '2026-11-17T11:19:33.489813+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T11:19:53.833659+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-ir08-extractor-estático-django-drf-y-sql

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-111910/context-review/task-ir08-extractor-estático-django-drf-y-sql/bundle/b131b8dba009c32bd4a243d69456735a4392be18f94b1296bad0f9dd480d4823/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Adjudicado: (1) el informe es el valor que devuelve la función pública de specir.extract (listas creados, sin cambios, cambiados y no derivados), sin CLI ni otro canal; (2) apply_batch de sldb valida RelationTypeDoc al escribir, y los RuleDoc se comprueban con sldb rules check --store .sldb --format json como en rules_findings de tests/models/test_blog_chain.py; cualquier hallazgo de nivel error hace fallar la prueba; (3) pruebas nuevas en tests/extract/, organización libre; (4) golden = los nodos y relaciones de backend y datos de tests/models/blog.py (ApiOperationDoc, HandlerDoc, DomainOperationDoc, PolicyDoc, StateDoc, DomainEntityDoc y TableDoc con handled_by, executes, governed_by, writes y persisted_in; transitions si hay fact), mismos tipos y relaciones, títulos libres salvo la ruta POST /posts/{id}/publish y la tabla posts; InterfaceControlDoc e InterfaceActionDoc son de IR09; (5) todas las anclas se comprueban antes de apply_batch: si una no coincide, ValueError con el ref y no se escribe nada
