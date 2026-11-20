---
sldb:
  by: agent
  at: '2026-11-20T20:53:02Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester-evidence-atom-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester@sha256:688174f39753459acedb6c8dfc49dcd96834e14e2ae18047aac46398f43e0f46
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: ead44108d20cc2dfffa530922a4d63fa2dfc8436170fa423a39fbae20ed67886
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas'
# ISO 8601 timestamp
created_at: '2026-11-20T20:53:01.656322+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T20:53:01.656322+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence atom of task-specir-extract-obtiene-el-source-hash-por-sldb-api-en-vez-de-leer-los-bytes-del-fuente-d1-del-tester

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
