---
sldb:
  by: agent
  at: '2026-11-25T19:50:34Z'
  authority: generated
  via: create_document
id: materialization-capacidad-7-validar-una-spec-y-sincronizarla-al-store
title: capacidad-7-validar-una-spec-y-sincronizarla-al-store tests/visual/test_api.py
source_atoms:
- CapabilityDoc:capacidad-7-validar-una-spec-y-sincronizarla-al-store
target_kind: test
target_identity: tests/visual/test_api.py::test_validate_passes
validation:
- python -m pytest -q tests/visual/test_api.py -k test_validate_passes
tags:
- system:ir
- topic:capacidades
---

# capacidad-7-validar-una-spec-y-sincronizarla-al-store tests/visual/test_api.py

## Intent

La prueba de aceptación de la capacidad 7 es tests/visual/test_api.py::test_validate_passes.
