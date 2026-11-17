---
sldb:
  by: agent
  at: '2026-11-17T14:38:13Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas-bundle-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas@sha256:fc0f36b0854708f310a829378049891e659bce5296de51342c27300d50559b4a
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-143721/context-review/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas/bundle/d912ae5f65cc159f2f2b3d568f30498d40d3747d79a280af2b8958218070d725/attempt-1
input_sha256: d912ae5f65cc159f2f2b3d568f30498d40d3747d79a280af2b8958218070d725
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: a7a65e1191c47ca8dacc7ebf03a50bf4d0b4fbcb2c29f0017eeee70e6697ae91
output_sha256: 763682423c18130e107545437b9001eac4cd3a6ba23a12358ebb03d2ece66fc7
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Adjudicado: (1) hoy no hay validadores de lote: no se agrega ninguno; mcp_extension.py
  no se toca y la comprobación es la de (e) (rules check y edges check tras undo);
  (2) el cambio ajeno lo hace apply_changes de la misma sesión u otra con un lote
  update que reponga el contenido anterior; para el caso stale, el cambio ajeno se
  hace con sldb.api.apply_batch fuera de la sesión MCP; (3) lote de nivel 1: crear
  un DomainEntityDoc, editar otro documento de dominio existente de la copia y crear
  un RelationDoc entre ellos con un tipo de relation_types.yaml; nivel 2: el mismo
  con un RuleDoc nuevo; (4) se prueban 0, 1 y 2, como fija (b); (5) el grep se juzga
  con el criterio (f): sus coincidencias se listan una a una en result-summary.md'
# ISO 8601 timestamp
created_at: '2026-11-17T14:37:53.287595+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T14:38:11.652416+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-143721/context-review/task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas/bundle/d912ae5f65cc159f2f2b3d568f30498d40d3747d79a280af2b8958218070d725/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Adjudicado: (1) hoy no hay validadores de lote: no se agrega ninguno; mcp_extension.py no se toca y la comprobación es la de (e) (rules check y edges check tras undo); (2) el cambio ajeno lo hace apply_changes de la misma sesión u otra con un lote update que reponga el contenido anterior; para el caso stale, el cambio ajeno se hace con sldb.api.apply_batch fuera de la sesión MCP; (3) lote de nivel 1: crear un DomainEntityDoc, editar otro documento de dominio existente de la copia y crear un RelationDoc entre ellos con un tipo de relation_types.yaml; nivel 2: el mismo con un RuleDoc nuevo; (4) se prueban 0, 1 y 2, como fija (b); (5) el grep se juzga con el criterio (f): sus coincidencias se listan una a una en result-summary.md
