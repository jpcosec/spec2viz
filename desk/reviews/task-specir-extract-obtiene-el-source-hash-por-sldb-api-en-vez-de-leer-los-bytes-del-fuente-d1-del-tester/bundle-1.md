---
sldb:
  by: agent
  at: '2026-11-17T15:57:45Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester@sha256:7294bddb73fbbc7c5aa2a3b6865399efcdec6e6b43454be6adc23d97df10c870
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-155724/context-review/task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester/bundle/9c23de7ce19db3bd769845030d33e2428006aeebd659f51d27d807b9a4cfa11c/attempt-1
input_sha256: 9c23de7ce19db3bd769845030d33e2428006aeebd659f51d27d807b9a4cfa11c
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 1ffd071b65f73c3b8b7ce9ba390938426856d470f72439a7cffcdfda253d2254
output_sha256: 41efee60fd9f088cc9dd8881da13a8cf9fc9497ca7da15f9c217d6b4ce915938
# pending | accepted | rejected | incomplete
verdict: accepted
reason: '1 y 4: resueltos en preflight-1 (code_facts; grep vacío sin filtrar). 2:
  tests/fixtures/blog_app, copiado a /dev/shm como hace tests/extract/extraction.py.
  3: el ref es la clave del fact en el plan, la misma que ya usa el ValueError actual
  de checked_blocks (f''{ref}: ...'').'
# ISO 8601 timestamp
created_at: '2026-11-17T15:57:33.466060+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T15:57:43.550804+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-155724/context-review/task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester/bundle/9c23de7ce19db3bd769845030d33e2428006aeebd659f51d27d807b9a4cfa11c/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: 1 y 4: resueltos en preflight-1 (code_facts; grep vacío sin filtrar). 2: tests/fixtures/blog_app, copiado a /dev/shm como hace tests/extract/extraction.py. 3: el ref es la clave del fact en el plan, la misma que ya usa el ValueError actual de checked_blocks (f'{ref}: ...').
