---
sldb:
  by: agent
  at: '2026-11-16T11:00:31Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a-preflight-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a@sha256:39d7d97e36dab7cdddf9d623acf2b0f270796e43032f36936d07535324971908
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261116-105938/context-review/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/preflight/6181b07c7773c7e478dddc157102f65fc1ae86ee7cea8176b7c55ce34273bd12/attempt-2
input_sha256: 6181b07c7773c7e478dddc157102f65fc1ae86ee7cea8176b7c55ce34273bd12
output_sha256: 993c596e87c20c91b0b59ec8eeb4744f2a39d447d3e4e6d88bce27c3bd7fc043
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Reformulación fiel. Precisiones: (1) <dir> y <ruta> son el directorio del
  proyecto temporal, y spec_store = <dir>/.sldb. En stores add se pasa spec_store
  tal cual, sin un .sldb duplicado. (2) Los llamadores son los que lista grep -n ''mount_copy(''
  tests/. (3) Las pruebas son las que lista grep -n ''federated_digest\|original_digest\|copy_digest''
  tests/. (4) El proyecto es spec_store.parent. El digest es un dict de ruta a sha256,
  igual que el de tree_digest y federated_digest: tree_digest(spec_store) más un sha256
  por cada .md bajo el proyecto (rglob), fusionados en el mismo dict. Los YAML de
  .sldb ya entran por tree_digest. (5) Vale lo de preflight-1 de la tarea: el ajuste
  admisible es cambiar de dónde salen los datos esperados, nunca una aserción sobre
  la respuesta del servidor.'
# ISO 8601 timestamp
created_at: '2026-11-16T11:00:13.858911+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T11:00:30.492168+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261116-105938/context-review/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/preflight/6181b07c7773c7e478dddc157102f65fc1ae86ee7cea8176b7c55ce34273bd12/attempt-2.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Reformulación fiel. Precisiones: (1) <dir> y <ruta> son el directorio del proyecto temporal, y spec_store = <dir>/.sldb. En stores add se pasa spec_store tal cual, sin un .sldb duplicado. (2) Los llamadores son los que lista grep -n 'mount_copy(' tests/. (3) Las pruebas son las que lista grep -n 'federated_digest\|original_digest\|copy_digest' tests/. (4) El proyecto es spec_store.parent. El digest es un dict de ruta a sha256, igual que el de tree_digest y federated_digest: tree_digest(spec_store) más un sha256 por cada .md bajo el proyecto (rglob), fusionados en el mismo dict. Los YAML de .sldb ya entran por tree_digest. (5) Vale lo de preflight-1 de la tarea: el ajuste admisible es cambiar de dónde salen los datos esperados, nunca una aserción sobre la respuesta del servidor.
