---
sldb:
  by: agent
  at: '2026-11-26T00:35:15Z'
  authority: generated
  via: create_document
id: materialization-invariante-depends-on-src-specir-models-domain-py
title: invariante-depends-on src-specir-models-domain-py
source_atoms:
- atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
target_kind: code
target_identity: src/specir/models/domain.py
validation:
- pytest -q tests/test_dependency_invariants.py tests/models/test_domain_models.py
tags:
- system:ir
- topic:invariante-depends-on
---

# invariante-depends-on src-specir-models-domain-py

## Intent

materializa en src/specir/models/domain.py el atom atom-un-invariante-entre-piezas-es-una-regla-sobre-los-nodos-de-specir
