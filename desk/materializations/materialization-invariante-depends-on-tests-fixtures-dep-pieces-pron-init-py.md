---
sldb:
  by: agent
  at: '2026-11-26T00:39:12Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-tests-fixtures-dep-pieces-pron-init-py
title: invariante-depends-on tests-fixtures-dep_pieces-pron-__init__-py
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: test
target_identity: tests/fixtures/dep_pieces/pron/__init__.py
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on tests-fixtures-dep_pieces-pron-__init__-py

## Intent

materializa en tests/fixtures/dep_pieces/pron/__init__.py el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
