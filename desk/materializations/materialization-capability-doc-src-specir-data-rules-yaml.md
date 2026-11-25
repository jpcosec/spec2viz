---
sldb:
  by: agent
  at: '2026-11-25T23:17:02Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-src-specir-data-rules-yaml
title: capability-doc src-specir-data-rules-yaml
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: code
target_identity: src/specir/data/rules.yaml
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc src-specir-data-rules-yaml

## Intent

materializa en src/specir/data/rules.yaml el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
