---
sldb:
  by: agent
  at: '2026-11-17T14:06:28Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir08-extractor-estático-django-drf-y-sql-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir08-extractor-estático-django-drf-y-sql@sha256:714ea9a93fbd78049b742685bc2c0d2cd16c5d16a6a6b3d42cfb03768b60526b
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f0bdf697d771a1bfe928abed38146e210938fb1fc80f156c8818e6e2c1889e1d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: No resolvable commit reference found.
# ISO 8601 timestamp
created_at: '2026-11-17T14:06:25.834969+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T14:06:25.834969+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-ir08-extractor-estático-django-drf-y-sql

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: (nothing found)

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: No resolvable commit reference found.
