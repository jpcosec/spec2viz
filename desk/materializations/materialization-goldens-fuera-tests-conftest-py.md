---
sldb:
  by: agent
  at: '2026-11-25T15:26:24Z'
  authority: generated
  via: create_document
id: materialization-goldens-fuera-tests-conftest-py
title: goldens-fuera tests-conftest-py
source_atoms:
- atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
target_kind: test
target_identity: tests/conftest.py
validation:
- pytest -q tests/visual
tags:
- system:ir
- topic:goldens-fuera
---

# goldens-fuera tests-conftest-py

## Intent

materializa en tests/conftest.py el atom atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
