---
sldb:
  by: agent
  at: '2026-11-25T15:27:22Z'
  authority: generated
  via: create_document
id: materialization-goldens-fuera-tests-visual-test-visual-names-py
title: goldens-fuera tests-visual-test_visual_names-py
source_atoms:
- atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
target_kind: test
target_identity: tests/visual/test_visual_names.py
validation:
- pytest -q tests/visual
tags:
- system:ir
- topic:goldens-fuera
---

# goldens-fuera tests-visual-test_visual_names-py

## Intent

materializa en tests/visual/test_visual_names.py el atom atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
