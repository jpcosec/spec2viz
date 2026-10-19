---
id: atom-multi-backend-renderers-where
title: Multi-Backend Renderers
five_wh_one_plus: where
tags:
- system:spec2viz
- topic:renderers
provenance: spec2viz/renderers/
---

# Multi-Backend Renderers

## Answer

Bajo spec2viz/renderers/. mermaid.py y plantuml.py (secuencia, estado, componentes, actividad, despliegue), class_diagram.py (clases, para ambos), d2.py, vega.py (matriz), antonia.py (HTML autocontenido con estetica antonIA), tree.py y graph_html.py (vistas HTML de arbol y grafo). renderers/__init__.py tiene RENDERER_MAP, EXT_MAP y DEFAULT_RENDERER por tipo de IR; render_to_file antepone la cabecera de trazabilidad a las salidas de texto.
