---
sldb:
  by: agent
  at: '2026-11-20T22:01:53Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir09-extractor-estático-react-tsx-y-contratos-de-api-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: '6121f69f9da3b924875991a2f432886ad58e2a02

  6a9bbdd0bc07a22bbff1bd7df7f781dbd8fa5f76'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir09-extractor-estático-react-tsx-y-contratos-de-api@sha256:1178dfccc9347c638e9e0f27ddd4dc6553428d116fae4c44b9c808726bcf2623
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 29e624ec079a96a9e7a6e523fcffdfc42d0323cf759cf17fdeab5353b109a635
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 6121f69f9da3b924875991a2f432886ad58e2a02

  6a9bbdd0bc07a22bbff1bd7df7f781dbd8fa5f76'
# ISO 8601 timestamp
created_at: '2026-11-20T22:01:51.608314+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T22:01:51.608314+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-ir09-extractor-estático-react-tsx-y-contratos-de-api

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 6121f69f9da3b924875991a2f432886ad58e2a02, 6a9bbdd0bc07a22bbff1bd7df7f781dbd8fa5f76

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 6121f69f9da3b924875991a2f432886ad58e2a02
6a9bbdd0bc07a22bbff1bd7df7f781dbd8fa5f76
