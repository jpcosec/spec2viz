---
sldb:
  by: agent
  at: '2026-11-25T14:56:01Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: f0c182d00cc8dd1cc0e85b09c8212bb314c62348
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr@sha256:16ba455e7336d4be90cd44e096a3ae2aab0e2511ab1d77d075673298fc911ebf
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 230b8544443c1089ebed708e8275a1d34c247a5990fadc0044dbd20a99a62633
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit f0c182d00cc8dd1cc0e85b09c8212bb314c62348'
# ISO 8601 timestamp
created_at: '2026-11-25T14:55:55.638433+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T14:55:55.638433+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: f0c182d00cc8dd1cc0e85b09c8212bb314c62348

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit f0c182d00cc8dd1cc0e85b09c8212bb314c62348
