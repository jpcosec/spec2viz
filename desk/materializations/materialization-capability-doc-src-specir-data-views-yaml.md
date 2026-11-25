---
sldb:
  by: agent
  at: '2026-11-25T23:17:57Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-src-specir-data-views-yaml
title: capability-doc src-specir-data-views-yaml
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: code
target_identity: src/specir/data/views.yaml
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc src-specir-data-views-yaml

## Intent

materializa en src/specir/data/views.yaml el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
