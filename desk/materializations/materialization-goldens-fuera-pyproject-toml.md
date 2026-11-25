---
sldb:
  by: agent
  at: '2026-11-25T15:26:18Z'
  authority: generated
  via: create_document
id: materialization-goldens-fuera-pyproject-toml
title: goldens-fuera pyproject-toml
source_atoms:
- atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
target_kind: code
target_identity: pyproject.toml
validation:
- pytest -q tests/visual
tags:
- system:ir
- topic:goldens-fuera
---

# goldens-fuera pyproject-toml

## Intent

materializa en pyproject.toml el atom atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion
