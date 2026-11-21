---
sldb:
  by: agent
  at: '2026-11-21T09:28:15Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: c47111de57c53e75a15a565ec945b73695de96c8
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac@sha256:c7fd34b49d6cdaac9d754ced1e28d42b2756bc631948ed92ff05005e85990106
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: acf6c6fad1c894ee6a4e75c906045a6c39a027366749321812bb688dbd5f1d37
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit c47111de57c53e75a15a565ec945b73695de96c8'
# ISO 8601 timestamp
created_at: '2026-11-21T09:28:13.448937+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T09:28:13.448937+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: c47111de57c53e75a15a565ec945b73695de96c8

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit c47111de57c53e75a15a565ec945b73695de96c8
