---
sldb:
  by: agent
  at: '2026-11-23T18:20:05Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-retiro-docs-spec2viz-matriz-de-cobertura-md

  materialization-retiro-tests-visual-test-retirement-gate-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita@sha256:55e68830499305ff64160a46e1e730b41d9f88868b72f98824148975798a312c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 8c375b08194b3ef0d1825ebfa5239f42ceacbebc345ee4fdaace8b0c86986303
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-retiro-docs-spec2viz-matriz-de-cobertura-md

  materialization-retiro-tests-visual-test-retirement-gate-py'
# ISO 8601 timestamp
created_at: '2026-11-23T18:19:55.543728+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T18:19:55.543728+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-retiro-docs-spec2viz-matriz-de-cobertura-md, materialization-retiro-tests-visual-test-retirement-gate-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-retiro-docs-spec2viz-matriz-de-cobertura-md
materialization-retiro-tests-visual-test-retirement-gate-py
