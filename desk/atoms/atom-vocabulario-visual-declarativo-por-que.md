---
id: atom-vocabulario-visual-declarativo-por-que
title: 'Vocabulario visual declarativo: por que'
five_wh_one_plus: why
tags:
- system:spec2viz
- topic:notation
provenance: docs/notation-contract.md
---

# Vocabulario visual declarativo: por que

## Answer

graph_ui dibujaba infiriendo del payload con una tabla fija clase a color, y las reglas de dibujo de spec2viz vivian en tablas de los renderers. Con la notacion como datos, toda regla nueva es un YAML, el mismo para spec2viz y para graph_ui, y spec2viz completo se muestra sobre graph_ui sin un if por notacion en ningun lado (ADR 2026-10-17).
