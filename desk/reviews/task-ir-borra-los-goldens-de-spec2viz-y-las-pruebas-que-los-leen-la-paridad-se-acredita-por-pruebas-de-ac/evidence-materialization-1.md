---
sldb:
  by: agent
  at: '2026-11-25T15:27:34Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-goldens-fuera-pyproject-toml

  materialization-goldens-fuera-tests-conftest-py

  materialization-goldens-fuera-tests-visual-test-cli-py

  materialization-goldens-fuera-tests-visual-test-lint-mermaid-py

  materialization-goldens-fuera-tests-visual-test-refs-models-py

  materialization-goldens-fuera-tests-visual-test-render-cases-py

  materialization-goldens-fuera-tests-visual-test-render-commands-py

  materialization-goldens-fuera-tests-visual-test-render-projections-py

  materialization-goldens-fuera-tests-visual-test-renderers-py

  materialization-goldens-fuera-tests-visual-test-resources-py

  materialization-goldens-fuera-tests-visual-test-schema-py

  materialization-goldens-fuera-tests-visual-test-visual-names-py

  materialization-parity-goldens-pyproject-toml

  materialization-retiro-tests-visual-test-cli-py

  materialization-retiro-tests-visual-test-lint-mermaid-py

  materialization-retiro-tests-visual-test-render-cases-py

  materialization-retiro-tests-visual-test-render-commands-py

  materialization-retiro-tests-visual-test-resources-py

  materialization-retiro-tests-visual-test-schema-py

  materialization-retiro-tests-visual-test-visual-names-py

  materialization-specir-package-declaration

  materialization-specir-test-store-copy-and-mcp-session

  materialization-specir-workspace-tests-conftest-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac@sha256:b818b50fa46ec47a817fead5728fe47473e854d3c160eb5bef4a12a0c61b1782
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 545abc9aa29de78d31d18b73bfd1f76f2cc6bd5303d3ef16e22318932541e5cb
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-goldens-fuera-pyproject-toml

  materialization-goldens-fuera-tests-conftest-py

  materialization-goldens-fuera-tests-visual-test-cli-py

  materialization-goldens-fuera-tests-visual-test-lint-mermaid-py

  materialization-goldens-fuera-tests-visual-test-refs-models-py

  materialization-goldens-fuera-tests-visual-test-render-cases-py

  materialization-goldens-fuera-tests-visual-test-render-commands-py

  materialization-goldens-fuera-tests-visual-test-render-projections-py

  materialization-goldens-fuera-tests-visual-test-renderers-py

  materialization-goldens-fuera-tests-visual-test-resources-py

  materialization-goldens-fuera-tests-visual-test-schema-py

  materialization-goldens-fuera-tests-visual-test-visual-names-py

  materialization-parity-goldens-pyproject-toml

  materialization-retiro-tests-visual-test-cli-py

  materialization-retiro-tests-visual-test-lint-mermaid-py

  materialization-retiro-tests-visual-test-render-cases-py

  materialization-retiro-tests-visual-test-render-commands-py

  materialization-retiro-tests-visual-test-resources-py

  materialization-retiro-tests-visual-test-schema-py

  materialization-retiro-tests-visual-test-visual-names-py

  materialization-specir-package-declaration

  materialization-specir-test-store-copy-and-mcp-session

  materialization-specir-workspace-tests-conftest-py'
# ISO 8601 timestamp
created_at: '2026-11-25T15:27:27.945803+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T15:27:27.945803+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-goldens-fuera-pyproject-toml, materialization-goldens-fuera-tests-conftest-py, materialization-goldens-fuera-tests-visual-test-cli-py, materialization-goldens-fuera-tests-visual-test-lint-mermaid-py, materialization-goldens-fuera-tests-visual-test-refs-models-py, materialization-goldens-fuera-tests-visual-test-render-cases-py, materialization-goldens-fuera-tests-visual-test-render-commands-py, materialization-goldens-fuera-tests-visual-test-render-projections-py, materialization-goldens-fuera-tests-visual-test-renderers-py, materialization-goldens-fuera-tests-visual-test-resources-py, materialization-goldens-fuera-tests-visual-test-schema-py, materialization-goldens-fuera-tests-visual-test-visual-names-py, materialization-parity-goldens-pyproject-toml, materialization-retiro-tests-visual-test-cli-py, materialization-retiro-tests-visual-test-lint-mermaid-py, materialization-retiro-tests-visual-test-render-cases-py, materialization-retiro-tests-visual-test-render-commands-py, materialization-retiro-tests-visual-test-resources-py, materialization-retiro-tests-visual-test-schema-py, materialization-retiro-tests-visual-test-visual-names-py, materialization-specir-package-declaration, materialization-specir-test-store-copy-and-mcp-session, materialization-specir-workspace-tests-conftest-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-goldens-fuera-pyproject-toml
materialization-goldens-fuera-tests-conftest-py
materialization-goldens-fuera-tests-visual-test-cli-py
materialization-goldens-fuera-tests-visual-test-lint-mermaid-py
materialization-goldens-fuera-tests-visual-test-refs-models-py
materialization-goldens-fuera-tests-visual-test-render-cases-py
materialization-goldens-fuera-tests-visual-test-render-commands-py
materialization-goldens-fuera-tests-visual-test-render-projections-py
materialization-goldens-fuera-tests-visual-test-renderers-py
materialization-goldens-fuera-tests-visual-test-resources-py
materialization-goldens-fuera-tests-visual-test-schema-py
materialization-goldens-fuera-tests-visual-test-visual-names-py
materialization-parity-goldens-pyproject-toml
materialization-retiro-tests-visual-test-cli-py
materialization-retiro-tests-visual-test-lint-mermaid-py
materialization-retiro-tests-visual-test-render-cases-py
materialization-retiro-tests-visual-test-render-commands-py
materialization-retiro-tests-visual-test-resources-py
materialization-retiro-tests-visual-test-schema-py
materialization-retiro-tests-visual-test-visual-names-py
materialization-specir-package-declaration
materialization-specir-test-store-copy-and-mcp-session
materialization-specir-workspace-tests-conftest-py
