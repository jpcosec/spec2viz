---
sldb:
  by: agent
  at: '2026-11-25T23:28:17Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-tests-test-capabilities-as-nodes-py
title: capability-doc tests-test_capabilities_as_nodes-py
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: test
target_identity: tests/test_capabilities_as_nodes.py
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc tests-test_capabilities_as_nodes-py

## Intent

materializa en tests/test_capabilities_as_nodes.py el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
