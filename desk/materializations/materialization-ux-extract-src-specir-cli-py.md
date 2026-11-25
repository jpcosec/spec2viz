---
sldb:
  by: agent
  at: '2026-11-25T13:43:10Z'
  authority: generated
  via: create_document
id: materialization-ux-extract-src-specir-cli-py
title: ux-extract src-specir-cli-py
source_atoms:
- atom-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados
target_kind: code
target_identity: src/specir/cli.py
validation:
- pytest -q tests/extract/test_ux_extract_cli.py
tags:
- system:ir
- topic:ux-extract
---

# ux-extract src-specir-cli-py

## Intent

materializa en src/specir/cli.py el atom atom-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados
