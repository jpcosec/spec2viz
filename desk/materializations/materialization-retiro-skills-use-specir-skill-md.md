---
sldb:
  by: agent
  at: '2026-11-21T06:39:32Z'
  authority: generated
  via: create_document
id: materialization-retiro-skills-use-specir-skill-md
title: retiro skills-use-specir-SKILL-md
source_atoms:
- atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
target_kind: docs
target_identity: skills/use-specir/SKILL.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual/test_cli.py tests/test_matriz_cobertura_spec2viz.py
  tests/visual/test_retirement_gate.py
tags:
- system:ir
- topic:retiro
---

# retiro skills-use-specir-SKILL-md

## Intent

materializa en skills/use-specir/SKILL.md el atom atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate
