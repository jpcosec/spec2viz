---
sldb:
  by: agent
  at: '2026-11-16T16:01:33Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/test_matriz_cobertura_spec2viz.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5@sha256:c15416e74e2e8a47fecc422897cc0b275fa0c760d3a47ee36a96a19d31d503ef
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 8577af6cca9c262e9d6ba732fff40f0a0a2a37b470f45195fe2640b50f758740
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_matriz_cobertura_spec2viz.py'
# ISO 8601 timestamp
created_at: '2026-11-16T16:01:32.070353+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T16:01:32.070353+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_matriz_cobertura_spec2viz.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_matriz_cobertura_spec2viz.py
