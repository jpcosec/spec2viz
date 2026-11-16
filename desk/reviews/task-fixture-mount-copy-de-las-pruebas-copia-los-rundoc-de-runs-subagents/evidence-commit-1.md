---
sldb:
  by: agent
  at: '2026-11-16T13:53:38Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 9c30a40de7854b77c43c7b738765c3d41796ebaa
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents@sha256:43f09b39721ee252d24d047ada67c4c5092d7696f6f3d65db2e1c0e7a8024f64
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 6d3feea9bbf498a8ed3d2fc2aa5d2be7195572f0eb4f1b2b12c7646452e62226
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 9c30a40de7854b77c43c7b738765c3d41796ebaa'
# ISO 8601 timestamp
created_at: '2026-11-16T13:53:33.823795+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T13:53:33.823795+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 9c30a40de7854b77c43c7b738765c3d41796ebaa

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 9c30a40de7854b77c43c7b738765c3d41796ebaa
