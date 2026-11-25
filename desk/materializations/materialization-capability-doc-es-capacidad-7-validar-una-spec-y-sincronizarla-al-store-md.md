---
sldb:
  by: agent
  at: '2026-11-25T22:52:17Z'
  authority: generated
  via: create_document
id: materialization-capability-doc-es-capacidad-7-validar-una-spec-y-sincronizarla-al-store-md
title: capability-doc es-capacidad-7-validar-una-spec-y-sincronizarla-al-store-md
source_atoms:
- atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
target_kind: docs
target_identity: specir/capabilities/capacidad-7-validar-una-spec-y-sincronizarla-al-store.md
validation:
- pytest -q tests/models/test_domain_models.py
tags:
- system:ir
- topic:capability-doc
---

# capability-doc es-capacidad-7-validar-una-spec-y-sincronizarla-al-store-md

## Intent

materializa en specir/capabilities/capacidad-7-validar-una-spec-y-sincronizarla-al-store.md el atom atom-una-capacidad-del-dominio-declara-su-audiencia-y-su-prueba-de-aceptacion
