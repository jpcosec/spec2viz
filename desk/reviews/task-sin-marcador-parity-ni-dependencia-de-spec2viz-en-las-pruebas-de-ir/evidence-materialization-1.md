---
sldb:
  by: agent
  at: '2026-11-25T05:56:53Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-parity-goldens-pyproject-toml

  materialization-specir-package-declaration'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir@sha256:e77c0c2bf2c33a8c1e3ad20a0829cf66d0a2f92441bc73c73dadb455d581aff9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 6a9a83953306825fffe888c9362a9ba91048a3113d96a02e570b66d1456db861
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-parity-goldens-pyproject-toml

  materialization-specir-package-declaration'
# ISO 8601 timestamp
created_at: '2026-11-25T05:56:46.814494+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T05:56:46.814494+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-parity-goldens-pyproject-toml, materialization-specir-package-declaration

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-parity-goldens-pyproject-toml
materialization-specir-package-declaration
