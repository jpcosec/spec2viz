---
sldb:
  by: agent
  at: '2026-11-25T14:56:04Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr@sha256:16ba455e7336d4be90cd44e096a3ae2aab0e2511ab1d77d075673298fc911ebf
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 541931c97861392bf29f793d91895dd7517279facf90b23d8f30a8a1fabb3c62
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace'
# ISO 8601 timestamp
created_at: '2026-11-25T14:55:55.638433+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T14:55:55.638433+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence atom of task-las-pruebas-de-ir-encuentran-el-workspace-de-sldb-1-por-specir-workspace-y-no-por-el-directorio-padr

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace
