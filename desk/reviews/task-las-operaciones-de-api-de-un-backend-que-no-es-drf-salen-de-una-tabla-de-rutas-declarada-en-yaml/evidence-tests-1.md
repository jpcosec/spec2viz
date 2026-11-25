---
sldb:
  by: agent
  at: '2026-11-25T06:38:31Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/specir/extract/__init__.py

  src/specir/extract/plan.py

  src/specir/extract/routes.py

  src/specir/extract/write.py

  tests/extract/test_declared_routes.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml@sha256:0a596f2c3eb2a2ef698583701bfe95526d00f3de5b183b429a415d04d1b52254
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 1fedec0310c528fa9473f7dd8aee2a680cb8cadbf916c8cf24b4883142378a0d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/specir/extract/__init__.py

  src/specir/extract/plan.py

  src/specir/extract/routes.py

  src/specir/extract/write.py

  tests/extract/test_declared_routes.py'
# ISO 8601 timestamp
created_at: '2026-11-25T06:38:31.173391+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T06:38:31.173391+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-las-operaciones-de-api-de-un-backend-que-no-es-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/specir/extract/__init__.py, src/specir/extract/plan.py, src/specir/extract/routes.py, src/specir/extract/write.py, tests/extract/test_declared_routes.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/specir/extract/__init__.py
src/specir/extract/plan.py
src/specir/extract/routes.py
src/specir/extract/write.py
tests/extract/test_declared_routes.py
