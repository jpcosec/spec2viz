---
sldb:
  by: agent
  at: '2026-11-26T00:31:27Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-src-specir-extract-dependencies-py
title: invariante-depends-on src-specir-extract-dependencies-py
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: code
target_identity: src/specir/extract/dependencies.py
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on src-specir-extract-dependencies-py

## Intent

materializa en src/specir/extract/dependencies.py el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
