---
sldb:
  by: agent
  at: '2026-11-16T15:30:07Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir-gitignore-ignora-egg-info-y-pycache-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir-gitignore-ignora-egg-info-y-pycache@sha256:74f2d1abb7345c9b8be8e854e7d8d604e126c4a35e100a28d6627f9d1480f59c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 4155f1d271d604932873bf8d4b74c7d7f5082372acd31e1584e2f159585e11a3
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: Changed file has no atom/materialization link and no routed follow-up reference.
# ISO 8601 timestamp
created_at: '2026-11-16T15:29:56.329437+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T15:29:56.329437+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence atom of task-ir-gitignore-ignora-egg-info-y-pycache

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: (nothing found)

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Changed file has no atom/materialization link and no routed follow-up reference.
