---
sldb:
  by: agent
  at: '2026-11-25T23:08:47Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-ecir-rules-rule-specir-capability-has-an-acceptance-test-md
title: capability-doc ecir-rules-rule-specir-capability-has-an-acceptance-test-md
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: docs
target_identity: specir/rules/rule-specir-capability-has-an-acceptance-test.md
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc ecir-rules-rule-specir-capability-has-an-acceptance-test-md

## Intent

materializa en specir/rules/rule-specir-capability-has-an-acceptance-test.md el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
