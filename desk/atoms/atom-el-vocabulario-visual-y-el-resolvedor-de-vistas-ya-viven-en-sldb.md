---
sldb:
  by: agent
  at: '2026-11-11T22:25:36Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
title: El vocabulario visual y el resolvedor de vistas ya viven en SLDB
five_wh_one_plus: where
tags:
- system:specir
- system:sldb
- system:spec2viz
- topic:vistas
- layer:modelo
provenance: ../sldb-astryx/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/dag.yaml
---

# El vocabulario visual y el resolvedor de vistas ya viven en SLDB

## Answer

Desde el plan absorber-spec2viz-y-modelos-ui de SLDB (entregado el 2026-11-07), los modelos SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb/src/sldb/models/notation/, las notaciones y paletas builtin en sldb/src/sldb/notations/, y el resolvedor de vistas y proyecciones en sldb/src/sldb/api/notations/. Un alias en sldb/src/sldb/api/model_registry/model_reference.py resuelve las referencias antiguas spec2viz.sldb_models. specIR usa esas piezas desde SLDB y no las redefine. En spec2viz quedan, sin equivalente en SLDB, la autoría de specs YAML, los compiladores, los renderizadores, el catálogo y la sincronización de specs al store.
