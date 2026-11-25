---
sldb:
  by: agent
  at: '2026-11-25T13:32:21Z'
  authority: generated
  via: create_document
id: materialization-ui-esqueleto-ui-tsconfig-json
title: ui-esqueleto ui-tsconfig-json
source_atoms:
- atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve
target_kind: code
target_identity: ui/tsconfig.json
validation:
- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx
tags:
- system:ir
- topic:ui-esqueleto
---

# ui-esqueleto ui-tsconfig-json

## Intent

materializa en ui/tsconfig.json el atom atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve
