---
sldb:
  by: agent
  at: '2026-11-26T00:41:57Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-tests-test-dependency-invariants-py
title: invariante-depends-on tests-test_dependency_invariants-py
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: test
target_identity: tests/test_dependency_invariants.py
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on tests-test_dependency_invariants-py

## Intent

materializa en tests/test_dependency_invariants.py el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
