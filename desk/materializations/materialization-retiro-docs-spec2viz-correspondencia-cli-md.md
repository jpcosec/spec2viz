---
sldb:
  by: agent
  at: '2026-11-21T06:39:19Z'
  authority: generated
  via: create_document
id: materialization-retiro-docs-spec2viz-correspondencia-cli-md
title: retiro docs-spec2viz-correspondencia-cli-md
source_atoms:
- atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
target_kind: docs
target_identity: docs/spec2viz/correspondencia-cli.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual/test_cli.py tests/test_matriz_cobertura_spec2viz.py
  tests/visual/test_retirement_gate.py
tags:
- system:ir
- topic:retiro
---

# retiro docs-spec2viz-correspondencia-cli-md

## Intent

materializa en docs/spec2viz/correspondencia-cli.md el atom atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
