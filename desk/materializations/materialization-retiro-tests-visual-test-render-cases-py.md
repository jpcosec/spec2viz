---
sldb:
  by: agent
  at: '2026-11-21T06:40:09Z'
  authority: generated
  via: create_document
id: materialization-retiro-tests-visual-test-render-cases-py
title: retiro tests-visual-test_render_cases-py
source_atoms:
- atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
target_kind: test
target_identity: tests/visual/test_render_cases.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual/test_cli.py tests/test_matriz_cobertura_spec2viz.py
  tests/visual/test_retirement_gate.py
tags:
- system:ir
- topic:retiro
---

# retiro tests-visual-test_render_cases-py

## Intent

materializa en tests/visual/test_render_cases.py el atom atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
