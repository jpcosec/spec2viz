---
sldb:
  by: agent
  at: '2026-11-25T23:00:55Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-specir-relation-types-type-governed-by-md
title: capability-doc specir-relation-types-type-governed_by-md
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: docs
target_identity: specir/relation-types/type-governed_by.md
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc specir-relation-types-type-governed_by-md

## Intent

materializa en specir/relation-types/type-governed_by.md el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
