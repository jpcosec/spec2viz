---
sldb:
  by: agent
  at: '2026-11-25T23:30:55Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/specir/install.py

  src/specir/models/__init__.py

  src/specir/models/domain.py

  tests/conftest.py

  tests/models/test_domain_models.py

  tests/test_capabilities_as_nodes.py

  tests/test_mcp_extension.py

  tests/test_mcp_undo.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid@sha256:49bc08f60806649a2b36df4221941d3dc1359b74f0929725887cc4d2ffaf9b01
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 039e8be11596c67ddada949a650f37f829ae90fbd48e25baa33ec9160e58fd2f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/specir/install.py

  src/specir/models/__init__.py

  src/specir/models/domain.py

  tests/conftest.py

  tests/models/test_domain_models.py

  tests/test_capabilities_as_nodes.py

  tests/test_mcp_extension.py

  tests/test_mcp_undo.py'
# ISO 8601 timestamp
created_at: '2026-11-25T23:30:12.093682+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T23:30:12.093682+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/specir/install.py, src/specir/models/__init__.py, src/specir/models/domain.py, tests/conftest.py, tests/models/test_domain_models.py, tests/test_capabilities_as_nodes.py, tests/test_mcp_extension.py, tests/test_mcp_undo.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/specir/install.py
src/specir/models/__init__.py
src/specir/models/domain.py
tests/conftest.py
tests/models/test_domain_models.py
tests/test_capabilities_as_nodes.py
tests/test_mcp_extension.py
tests/test_mcp_undo.py
