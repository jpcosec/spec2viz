---
sldb:
  by: agent
  at: '2026-11-21T01:29:51Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir10-reglas-semánticas-y-análisis-de-impacto-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/specir/impact.py

  src/specir/mcp_extension.py

  src/specir/models/__init__.py

  src/specir/models/domain.py

  tests/models/test_domain_models.py

  tests/models/test_rules_and_impact.py

  tests/test_mcp_extension.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir10-reglas-semánticas-y-análisis-de-impacto@sha256:63633ee7dee8a04ef64ae54c1c3047721f00d9f9b7d63e17629685da3361eb55
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: d35e50c7971d418d8cb44ca73a6758a5a4120c15275c2aae528f4fef12972586
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/specir/impact.py

  src/specir/mcp_extension.py

  src/specir/models/__init__.py

  src/specir/models/domain.py

  tests/models/test_domain_models.py

  tests/models/test_rules_and_impact.py

  tests/test_mcp_extension.py'
# ISO 8601 timestamp
created_at: '2026-11-21T01:29:50.552259+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T01:29:50.552259+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-ir10-reglas-semánticas-y-análisis-de-impacto

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/specir/impact.py, src/specir/mcp_extension.py, src/specir/models/__init__.py, src/specir/models/domain.py, tests/models/test_domain_models.py, tests/models/test_rules_and_impact.py, tests/test_mcp_extension.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/specir/impact.py
src/specir/mcp_extension.py
src/specir/models/__init__.py
src/specir/models/domain.py
tests/models/test_domain_models.py
tests/models/test_rules_and_impact.py
tests/test_mcp_extension.py
