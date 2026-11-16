---
sldb:
  by: agent
  at: '2026-11-16T10:42:13Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a@sha256:a7fcf1169c2cb23fb7851f440a612b90e6a62fcddc8f246b87cbceb0f6b508e4
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261116-104117/context-review/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/preflight/88d097b4529df38a3e41bcc80f3f12deb04a2daffd7963931cb34fa2e18d2605/attempt-1
input_sha256: 88d097b4529df38a3e41bcc80f3f12deb04a2daffd7963931cb34fa2e18d2605
output_sha256: 330539035073132d66ab79354fec3a8e1093efea003dc7b1db9066704f19226b
# pending | accepted | rejected | incomplete
verdict: accepted
reason: Reformulación fiel. Las ambigüedades se resuelven leyendo tests/conftest.py,
  que el implementation_path manda leer completo. (1) Las pruebas de digests son las
  que usan original_digest, copy_digest_before, federated_digest o tree_digest en
  tests/test_mcp_extension.py (grep -n digest). (2) Un ajuste es admisible si solo
  cambia de dónde lee la prueba los datos esperados (el store temporal en vez de FEDERATED[SPEC_STORE]),
  y no si cambia o quita alguna aserción sobre la respuesta del servidor. (3) El store
  de deskops es FEDERATED['deskops'] = WORKSPACE/'deskops'/'.sldb', con alias deskops,
  y no cambia. (4) root es la variable root de mount_copy (la copia montada). (5)
  El .venv es el de la raíz de IR.
# ISO 8601 timestamp
created_at: '2026-11-16T10:41:29.785733+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T10:42:12.628399+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261116-104117/context-review/task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a/preflight/88d097b4529df38a3e41bcc80f3f12deb04a2daffd7963931cb34fa2e18d2605/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Reformulación fiel. Las ambigüedades se resuelven leyendo tests/conftest.py, que el implementation_path manda leer completo. (1) Las pruebas de digests son las que usan original_digest, copy_digest_before, federated_digest o tree_digest en tests/test_mcp_extension.py (grep -n digest). (2) Un ajuste es admisible si solo cambia de dónde lee la prueba los datos esperados (el store temporal en vez de FEDERATED[SPEC_STORE]), y no si cambia o quita alguna aserción sobre la respuesta del servidor. (3) El store de deskops es FEDERATED['deskops'] = WORKSPACE/'deskops'/'.sldb', con alias deskops, y no cambia. (4) root es la variable root de mount_copy (la copia montada). (5) El .venv es el de la raíz de IR.
