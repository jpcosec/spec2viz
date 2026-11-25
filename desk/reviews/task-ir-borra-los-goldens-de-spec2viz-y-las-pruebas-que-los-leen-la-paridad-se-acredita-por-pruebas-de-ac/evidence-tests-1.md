---
sldb:
  by: agent
  at: '2026-11-25T15:27:28Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'tests/conftest.py

  tests/visual/test_cli.py

  tests/visual/test_lint_mermaid.py

  tests/visual/test_refs_models.py

  tests/visual/test_render_cases.py

  tests/visual/test_render_commands.py

  tests/visual/test_render_projections.py

  tests/visual/test_renderers.py

  tests/visual/test_resources.py

  tests/visual/test_schema.py

  tests/visual/test_visual_names.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac@sha256:b818b50fa46ec47a817fead5728fe47473e854d3c160eb5bef4a12a0c61b1782
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: d2be83b85e9554cb8907d35a2f479c0b8bbe1c2977d565e644ca6160311dd81f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/conftest.py

  tests/visual/test_cli.py

  tests/visual/test_lint_mermaid.py

  tests/visual/test_refs_models.py

  tests/visual/test_render_cases.py

  tests/visual/test_render_commands.py

  tests/visual/test_render_projections.py

  tests/visual/test_renderers.py

  tests/visual/test_resources.py

  tests/visual/test_schema.py

  tests/visual/test_visual_names.py'
# ISO 8601 timestamp
created_at: '2026-11-25T15:27:27.945803+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T15:27:27.945803+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/conftest.py, tests/visual/test_cli.py, tests/visual/test_lint_mermaid.py, tests/visual/test_refs_models.py, tests/visual/test_render_cases.py, tests/visual/test_render_commands.py, tests/visual/test_render_projections.py, tests/visual/test_renderers.py, tests/visual/test_resources.py, tests/visual/test_schema.py, tests/visual/test_visual_names.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/conftest.py
tests/visual/test_cli.py
tests/visual/test_lint_mermaid.py
tests/visual/test_refs_models.py
tests/visual/test_render_cases.py
tests/visual/test_render_commands.py
tests/visual/test_render_projections.py
tests/visual/test_renderers.py
tests/visual/test_resources.py
tests/visual/test_schema.py
tests/visual/test_visual_names.py
