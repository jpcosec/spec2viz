---
sldb:
  by: agent
  at: '2026-11-15T15:45:41Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-specir-blog-chain-tests

  materialization-specir-cross-layer-rules

  materialization-specir-domain-model-tests

  materialization-specir-domain-models

  materialization-specir-install-command

  materialization-specir-models-package

  materialization-specir-relation-types'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog@sha256:da777a7ac947877e9f5994f543ecc27f3dd2a389a35e38f87f5e7307aca55f38
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 35a98caaebdb5aba253619f4d5b0aca2d3abb24b42e5b50f9bcdb1afb40e0c63
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: Changed file has no atom/materialization link and no routed follow-up reference.
# ISO 8601 timestamp
created_at: '2026-11-15T15:45:38.613353+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-15T15:45:38.613353+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-ir06-tipos-de-dominio-transversales-y-cadena-de-prueba-del-blog

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-specir-blog-chain-tests, materialization-specir-cross-layer-rules, materialization-specir-domain-model-tests, materialization-specir-domain-models, materialization-specir-install-command, materialization-specir-models-package, materialization-specir-relation-types

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Changed file has no atom/materialization link and no routed follow-up reference.
