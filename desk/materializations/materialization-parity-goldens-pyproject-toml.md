---
sldb:
  by: agent
  at: '2026-11-25T05:56:41Z'
  authority: generated
  via: create_document
id: materialization-parity-goldens-pyproject-toml
title: parity-goldens pyproject-toml
source_atoms:
- atom-las-pruebas-de-ir-no-dependen-de-spec2viz-el-marcador-parity-compara-contra-goldens
target_kind: code
target_identity: pyproject.toml
validation:
- pytest -q -m parity tests/visual
tags:
- system:ir
- topic:parity-goldens
---

# parity-goldens pyproject-toml

## Intent

materializa en pyproject.toml el atom atom-las-pruebas-de-ir-no-dependen-de-spec2viz-el-marcador-parity-compara-contra-goldens
