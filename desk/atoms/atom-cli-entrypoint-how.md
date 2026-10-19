---
id: atom-cli-entrypoint-how
title: CLI Entrypoint
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:cli
provenance: spec2viz/cli.py
---

# CLI Entrypoint

## Answer

Es un grupo de Click con tres subgrupos. 'spec2viz diagram' (render, validate, lint, schema, generate, from-graph, sync) carga el YAML con spec2viz.loader, lo valida, compila la IR y la manda al renderer pedido, o lo sincroniza al store sldb. 'spec2viz notation' (list, validate, sync, view) maneja el vocabulario visual (NotationDoc, GlyphDoc, LinkDoc) y resuelve la vista de un spec. 'spec2viz catalog' (build, sync, serve, schema) sincroniza un vistas.yml al store o construye el bundle HTML estatico. 'spec2viz about' explica el flujo. Los comandos planos render, validate, lint, schema y build siguen como alias legados de los de diagram y catalog.
