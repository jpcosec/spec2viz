---
sldb:
  by: agent
  at: '2026-11-26T00:37:08Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-tests-fixtures-dep-pieces-graph-ui-app-py
title: invariante-depends-on tests-fixtures-dep_pieces-graph_ui-app-py
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: test
target_identity: tests/fixtures/dep_pieces/graph_ui/app.py
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on tests-fixtures-dep_pieces-graph_ui-app-py

## Intent

materializa en tests/fixtures/dep_pieces/graph_ui/app.py el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
