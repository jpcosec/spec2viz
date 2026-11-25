---
sldb:
  by: agent
  at: '2026-11-25T23:15:13Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-specir-views-view-specir-capabilities-md
title: capability-doc specir-views-view-specir-capabilities-md
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: docs
target_identity: specir/views/view-specir-capabilities.md
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc specir-views-view-specir-capabilities-md

## Intent

materializa en specir/views/view-specir-capabilities.md el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
