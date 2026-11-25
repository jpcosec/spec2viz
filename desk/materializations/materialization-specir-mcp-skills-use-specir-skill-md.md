---
sldb:
  by: agent
  at: '2026-11-25T03:37:51Z'
  authority: generated
  via: create_document
id: materialization-specir-mcp-skills-use-specir-skill-md
title: specir-mcp skills-use-specir-SKILL-md
source_atoms:
- atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
target_kind: docs
target_identity: skills/use-specir/SKILL.md
validation:
- pytest -q tests/test_cli_mcp.py
tags:
- system:ir
- topic:specir-mcp
---

# specir-mcp skills-use-specir-SKILL-md

## Intent

materializa en skills/use-specir/SKILL.md el atom atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
