---
sldb:
  by: agent
  at: '2026-11-25T13:43:39Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 1f196cb189df9e80f7ccb4a6de420e3218583d28
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados@sha256:928454d609de53d8b4738ef9a415dfe9a96cc2a7ac7b81c3cc722f61adbad3ed
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: c108dbedcf74a477d46b448a628defa12e2bf5873afc295bd01dbbda81541252
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 1f196cb189df9e80f7ccb4a6de420e3218583d28'
# ISO 8601 timestamp
created_at: '2026-11-25T13:43:36.312359+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T13:43:36.312359+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 1f196cb189df9e80f7ccb4a6de420e3218583d28

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 1f196cb189df9e80f7ccb4a6de420e3218583d28
