---
sldb:
  by: agent
  at: '2026-11-25T13:31:58Z'
  authority: generated
  via: create_document
id: materialization-ui-esqueleto-ui-src-shell-css
title: ui-esqueleto ui-src-shell-css
source_atoms:
- atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve
target_kind: code
target_identity: ui/src/shell.css
validation:
- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx
tags:
- system:ir
- topic:ui-esqueleto
---

# ui-esqueleto ui-src-shell-css

## Intent

materializa en ui/src/shell.css el atom atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve
