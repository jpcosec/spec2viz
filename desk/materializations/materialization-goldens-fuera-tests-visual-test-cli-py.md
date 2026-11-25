---
sldb:
  by: agent
  at: '2026-11-25T15:26:30Z'
  authority: generated
  via: create_document
id: materialization-goldens-fuera-tests-visual-test-cli-py
title: goldens-fuera tests-visual-test_cli-py
source_atoms:
- atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
target_kind: test
target_identity: tests/visual/test_cli.py
validation:
- pytest -q tests/visual
tags:
- system:ir
- topic:goldens-fuera
---

# goldens-fuera tests-visual-test_cli-py

## Intent

materializa en tests/visual/test_cli.py el atom atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
