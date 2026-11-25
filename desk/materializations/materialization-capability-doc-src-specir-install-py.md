---
sldb:
  by: agent
  at: '2026-11-25T23:18:52Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-src-specir-install-py
title: capability-doc src-specir-install-py
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: code
target_identity: src/specir/install.py
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc src-specir-install-py

## Intent

materializa en src/specir/install.py el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
