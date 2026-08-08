---
id: atom-spec2viz-multi-backend-rendering
title: Multi-Backend Rendering Strategy
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:renderers
provenance: README.md
---

# Multi-Backend Rendering Strategy

## Answer

`spec2viz` soporta la proyección de un mismo modelo de datos YAML hacia múltiples motores visuales (`mermaid`, `plantuml`, `d2`, `vega`). Cada renderizador en `spec2viz.renderers` implementa el patrón Visitor sobre las estructuras de la Representación Intermedia (`IR`). Esto permite generar salidas Mermaid para previsualización directa en GitHub/web, PlantUML para documentación empresarial legada o SVG/D2 para diagramación avanzada, todo derivado de una única fuente de verdad YAML.
