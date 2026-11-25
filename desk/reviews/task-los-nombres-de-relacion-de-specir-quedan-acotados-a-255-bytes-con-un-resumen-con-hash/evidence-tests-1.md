---
sldb:
  by: agent
  at: '2026-11-25T12:37:58Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/specir/extract/plan.py

  tests/extract/test_edge_name_bounded.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash@sha256:04f9d737e36e97a2485dcc580efeec559183342508607ad439646a4ed9a7da04
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: c9b36d90c831ffe6aa5d930058313c0c44c4a323afaa14569adbd8c8c595bb5e
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/specir/extract/plan.py

  tests/extract/test_edge_name_bounded.py'
# ISO 8601 timestamp
created_at: '2026-11-25T12:37:58.104055+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T12:37:58.104055+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/specir/extract/plan.py, tests/extract/test_edge_name_bounded.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/specir/extract/plan.py
tests/extract/test_edge_name_bounded.py
