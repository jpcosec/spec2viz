---
sldb:
  by: agent
  at: '2026-11-25T14:55:03Z'
  authority: generated
  via: create_document
id: atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace
title: Las pruebas de IR encuentran el workspace por SPECIR_WORKSPACE
five_wh_one_plus: how
tags:
- system:ir
- topic:specir-workspace
---

# Las pruebas de IR encuentran el workspace por SPECIR_WORKSPACE

## Answer

tests/conftest.py resuelve el workspace de SLDB_1 con workspace_root(): SPECIR_WORKSPACE si esta definida, si no REPO.parent; asi la suite corre desde la copia del integrate.
