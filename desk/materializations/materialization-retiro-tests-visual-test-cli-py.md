---
sldb:
  by: agent
  at: '2026-11-21T06:39:56Z'
  authority: generated
  via: create_document
id: materialization-retiro-tests-visual-test-cli-py
title: retiro tests-visual-test_cli-py
source_atoms:
- atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
target_kind: test
target_identity: tests/visual/test_cli.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual/test_cli.py tests/test_matriz_cobertura_spec2viz.py
  tests/visual/test_retirement_gate.py
tags:
- system:ir
- topic:retiro
---

# retiro tests-visual-test_cli-py

## Intent

materializa en tests/visual/test_cli.py el atom atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
