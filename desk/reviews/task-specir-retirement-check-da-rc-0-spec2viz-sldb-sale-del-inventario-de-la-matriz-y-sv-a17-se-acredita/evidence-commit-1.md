---
sldb:
  by: agent
  at: '2026-11-23T18:19:59Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 'a12456204c4f5bf0895830efa6d262fe9298e75d

  b3e387b805202397b2ce674c741a05690f96f6b3'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita@sha256:55e68830499305ff64160a46e1e730b41d9f88868b72f98824148975798a312c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 8b37f157238d223a06c16ed3c778adf313b2b6507b0bb9299bc8180bf34e4bae
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit a12456204c4f5bf0895830efa6d262fe9298e75d

  b3e387b805202397b2ce674c741a05690f96f6b3'
# ISO 8601 timestamp
created_at: '2026-11-23T18:19:55.543728+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T18:19:55.543728+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-specir-retirement-check-da-rc-0-spec2viz-sldb-sale-del-inventario-de-la-matriz-y-sv-a17-se-acredita

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: a12456204c4f5bf0895830efa6d262fe9298e75d, b3e387b805202397b2ce674c741a05690f96f6b3

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit a12456204c4f5bf0895830efa6d262fe9298e75d
b3e387b805202397b2ce674c741a05690f96f6b3
