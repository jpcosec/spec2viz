---
sldb:
  by: agent
  at: '2026-11-25T14:08:44Z'
  authority: generated
  via: create_document
id: materialization-ui-cascaron-ui-src-shell-css
title: ui-cascaron ui-src-shell-css
source_atoms:
- atom-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta
target_kind: code
target_identity: ui/src/shell.css
validation:
- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx
tags:
- system:ir
- topic:ui-cascaron
---

# ui-cascaron ui-src-shell-css

## Intent

materializa en ui/src/shell.css el atom atom-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta
