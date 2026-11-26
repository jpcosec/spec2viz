---
sldb:
  by: agent
  at: '2026-11-26T00:41:05Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-tests-models-test-domain-models-py
title: invariante-depends-on tests-models-test_domain_models-py
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: test
target_identity: tests/models/test_domain_models.py
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on tests-models-test_domain_models-py

## Intent

materializa en tests/models/test_domain_models.py el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
