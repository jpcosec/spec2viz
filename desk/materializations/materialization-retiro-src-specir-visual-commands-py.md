---
sldb:
  by: agent
  at: '2026-11-21T06:39:45Z'
  authority: generated
  via: create_document
id: materialization-retiro-src-specir-visual-commands-py
title: retiro src-specir-visual-commands-py
source_atoms:
- atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
target_kind: code
target_identity: src/specir/visual/commands.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual/test_cli.py tests/test_matriz_cobertura_spec2viz.py
  tests/visual/test_retirement_gate.py
tags:
- system:ir
- topic:retiro
---

# retiro src-specir-visual-commands-py

## Intent

materializa en src/specir/visual/commands.py el atom atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
