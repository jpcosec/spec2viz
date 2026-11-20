---
sldb:
  by: agent
  at: '2026-11-20T22:01:52Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir09-extractor-estático-react-tsx-y-contratos-de-api-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/specir/extract/__init__.py

  src/specir/extract/plan.py

  src/specir/extract/react_tsx.py

  tests/extract/test_frontend_extraction.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir09-extractor-estático-react-tsx-y-contratos-de-api@sha256:1178dfccc9347c638e9e0f27ddd4dc6553428d116fae4c44b9c808726bcf2623
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: e15dc2e83cc512718463719af58c707a20d49dfebfc74ced1d95fd7c3749add8
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/specir/extract/__init__.py

  src/specir/extract/plan.py

  src/specir/extract/react_tsx.py

  tests/extract/test_frontend_extraction.py'
# ISO 8601 timestamp
created_at: '2026-11-20T22:01:51.608314+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T22:01:51.608314+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-ir09-extractor-estático-react-tsx-y-contratos-de-api

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/specir/extract/__init__.py, src/specir/extract/plan.py, src/specir/extract/react_tsx.py, tests/extract/test_frontend_extraction.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/specir/extract/__init__.py
src/specir/extract/plan.py
src/specir/extract/react_tsx.py
tests/extract/test_frontend_extraction.py
