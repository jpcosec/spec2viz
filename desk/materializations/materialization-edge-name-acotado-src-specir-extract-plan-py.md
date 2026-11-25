---
sldb:
  by: agent
  at: '2026-11-25T12:37:45Z'
  authority: generated
  via: create_document
id: materialization-edge-name-acotado-src-specir-extract-plan-py
title: edge-name-acotado src-specir-extract-plan-py
source_atoms:
- atom-los-nombres-de-relacion-de-specir-quedan-acotados-con-un-resumen-con-hash
target_kind: code
target_identity: src/specir/extract/plan.py
validation:
- pytest -q tests/extract/test_edge_name_bounded.py
tags:
- system:ir
- topic:edge-name-acotado
---

# edge-name-acotado src-specir-extract-plan-py

## Intent

materializa en src/specir/extract/plan.py el atom atom-los-nombres-de-relacion-de-specir-quedan-acotados-con-un-resumen-con-hash
