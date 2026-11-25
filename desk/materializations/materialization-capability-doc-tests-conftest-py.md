---
sldb:
  by: agent
  at: '2026-11-25T23:26:30Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-tests-conftest-py
title: capability-doc tests-conftest-py
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: test
target_identity: tests/conftest.py
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc tests-conftest-py

## Intent

materializa en tests/conftest.py el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
