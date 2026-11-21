---
sldb:
  by: agent
  at: '2026-11-21T09:28:13Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'tests/test_matriz_cobertura_spec2viz.py

  tests/visual/oracle.py

  tests/visual/parity.py

  tests/visual/render_parity.py

  tests/visual/test_catalog_parity.py

  tests/visual/test_cli.py

  tests/visual/test_lint_mermaid.py

  tests/visual/test_render_cases.py

  tests/visual/test_render_commands.py

  tests/visual/test_render_parity.py

  tests/visual/test_resources.py

  tests/visual/test_schema.py

  tests/visual/test_sync_generation_parity.py

  tests/visual/test_visual_names.py

  tests/visual/test_visual_parity.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac@sha256:c7fd34b49d6cdaac9d754ced1e28d42b2756bc631948ed92ff05005e85990106
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 4f43f7494a4946d6b0642f6fa9243894a7aeb67b4268b47896038730976c41b4
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_matriz_cobertura_spec2viz.py

  tests/visual/oracle.py

  tests/visual/parity.py

  tests/visual/render_parity.py

  tests/visual/test_catalog_parity.py

  tests/visual/test_cli.py

  tests/visual/test_lint_mermaid.py

  tests/visual/test_render_cases.py

  tests/visual/test_render_commands.py

  tests/visual/test_render_parity.py

  tests/visual/test_resources.py

  tests/visual/test_schema.py

  tests/visual/test_sync_generation_parity.py

  tests/visual/test_visual_names.py

  tests/visual/test_visual_parity.py'
# ISO 8601 timestamp
created_at: '2026-11-21T09:28:13.448937+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T09:28:13.448937+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_matriz_cobertura_spec2viz.py, tests/visual/oracle.py, tests/visual/parity.py, tests/visual/render_parity.py, tests/visual/test_catalog_parity.py, tests/visual/test_cli.py, tests/visual/test_lint_mermaid.py, tests/visual/test_render_cases.py, tests/visual/test_render_commands.py, tests/visual/test_render_parity.py, tests/visual/test_resources.py, tests/visual/test_schema.py, tests/visual/test_sync_generation_parity.py, tests/visual/test_visual_names.py, tests/visual/test_visual_parity.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_matriz_cobertura_spec2viz.py
tests/visual/oracle.py
tests/visual/parity.py
tests/visual/render_parity.py
tests/visual/test_catalog_parity.py
tests/visual/test_cli.py
tests/visual/test_lint_mermaid.py
tests/visual/test_render_cases.py
tests/visual/test_render_commands.py
tests/visual/test_render_parity.py
tests/visual/test_resources.py
tests/visual/test_schema.py
tests/visual/test_sync_generation_parity.py
tests/visual/test_visual_names.py
tests/visual/test_visual_parity.py
