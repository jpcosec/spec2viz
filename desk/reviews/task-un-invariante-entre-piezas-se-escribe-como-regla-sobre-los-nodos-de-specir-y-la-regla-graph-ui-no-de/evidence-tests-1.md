---
sldb:
  by: agent
  at: '2026-11-26T00:42:50Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/specir/cli.py

  src/specir/extract/__init__.py

  src/specir/extract/dependencies.py

  src/specir/extract/plan.py

  src/specir/extract/write.py

  src/specir/models/__init__.py

  src/specir/models/domain.py

  tests/fixtures/dep_pieces/graph_ui/__init__.py

  tests/fixtures/dep_pieces/graph_ui/app.py

  tests/fixtures/dep_pieces/graph_ui/view.py

  tests/fixtures/dep_pieces/pron/__init__.py

  tests/fixtures/dep_pieces/pron/core.py

  tests/models/test_domain_models.py

  tests/test_dependency_invariants.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de@sha256:2fff595b5139427518ba99a8acda1bfeec46bb5b7c41740660e4af1bb2093c50
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 411b8fb2b6dcb68249f16bed84ecf27e05820dc3216eff84a3ba2159e5b8cbe2
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/specir/cli.py

  src/specir/extract/__init__.py

  src/specir/extract/dependencies.py

  src/specir/extract/plan.py

  src/specir/extract/write.py

  src/specir/models/__init__.py

  src/specir/models/domain.py

  tests/fixtures/dep_pieces/graph_ui/__init__.py

  tests/fixtures/dep_pieces/graph_ui/app.py

  tests/fixtures/dep_pieces/graph_ui/view.py

  tests/fixtures/dep_pieces/pron/__init__.py

  tests/fixtures/dep_pieces/pron/core.py

  tests/models/test_domain_models.py

  tests/test_dependency_invariants.py'
# ISO 8601 timestamp
created_at: '2026-11-26T00:42:07.710674+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-26T00:42:07.710674+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-un-invariante-entre-piezas-se-escribe-como-regla-sobre-los-nodos-de-specir-y-la-regla-graph-ui-no-de

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/specir/cli.py, src/specir/extract/__init__.py, src/specir/extract/dependencies.py, src/specir/extract/plan.py, src/specir/extract/write.py, src/specir/models/__init__.py, src/specir/models/domain.py, tests/fixtures/dep_pieces/graph_ui/__init__.py, tests/fixtures/dep_pieces/graph_ui/app.py, tests/fixtures/dep_pieces/graph_ui/view.py, tests/fixtures/dep_pieces/pron/__init__.py, tests/fixtures/dep_pieces/pron/core.py, tests/models/test_domain_models.py, tests/test_dependency_invariants.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/specir/cli.py
src/specir/extract/__init__.py
src/specir/extract/dependencies.py
src/specir/extract/plan.py
src/specir/extract/write.py
src/specir/models/__init__.py
src/specir/models/domain.py
tests/fixtures/dep_pieces/graph_ui/__init__.py
tests/fixtures/dep_pieces/graph_ui/app.py
tests/fixtures/dep_pieces/graph_ui/view.py
tests/fixtures/dep_pieces/pron/__init__.py
tests/fixtures/dep_pieces/pron/core.py
tests/models/test_domain_models.py
tests/test_dependency_invariants.py
