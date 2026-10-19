---
id: atom-multi-backend-renderers-what
title: Multi-Backend Renderers
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:renderers
provenance: spec2viz/renderers/
---

# Multi-Backend Renderers

## Answer

Los Multi-Backend Renderers traducen un objeto IR en una salida concreta. Mermaid, PlantUML, D2, Vega, JSON, y HTML (antonia-html, tree, graph). Son la ruta de export estatico; la superficie viva es graph_ui, que no usa estos renderers sino la notacion declarada (NotationDoc, GlyphDoc, LinkDoc) y la vista de spec2viz notation view.
