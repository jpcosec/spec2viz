---
sldb:
  by: agent
  at: '2026-11-25T13:30:58Z'
  authority: generated
  via: create_document
id: materialization-ui-esqueleto-ui-package-json
title: ui-esqueleto ui-package-json
source_atoms:
- atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve
target_kind: code
target_identity: ui/package.json
validation:
- cd ui && npx tsc --noEmit && npx vitest run src/Shell.test.tsx
tags:
- system:ir
- topic:ui-esqueleto
---

# ui-esqueleto ui-package-json

## Intent

materializa en ui/package.json el atom atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve
