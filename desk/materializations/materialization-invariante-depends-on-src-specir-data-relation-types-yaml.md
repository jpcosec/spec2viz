---
sldb:
  by: agent
  at: '2026-11-26T00:27:47Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-src-specir-data-relation-types-yaml
title: invariante-depends-on src-specir-data-relation_types-yaml
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: code
target_identity: src/specir/data/relation_types.yaml
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on src-specir-data-relation_types-yaml

## Intent

materializa en src/specir/data/relation_types.yaml el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
