---
id: atom-spec2viz-deskops-workflow-integration-contract
title: Spec2viz Deskops Workflow Integration Contract
five_wh_one_plus: how
tags:
- system:spec2viz
- system:deskops
- topic:integration
- topic:adr
provenance: spec2viz/deskops.py
---

# Spec2viz Deskops Workflow Integration Contract

## Answer

El contrato de integracion entre spec2viz y deskops define como los registros de arquitectura (vistas.yml) se compilan en paquetes HTML interactivos, en tres partes. Parseo de atomos 5WH1+: spec2viz/deskops.py (parse_atoms) escanea desk/atoms/*.md, extrae el frontmatter YAML y clasifica el contenido en las siete dimensiones (what, why, how, how_not, when, where, for_whom), indexadas por titulo normalizado en window.ATOMS_DB. Orquestacion de vistas: render_deskops procesa vistas.yml, carga los diagramas proyectados (.mmd, .svg, .html) y genera la navegacion por categorias () y las secciones (). Inyeccion y vinculacion dinamica: la plantilla recibe window.ATOMS_DB y el navegador registra hover y click sobre los nodos de los diagramas para mostrar tarjetas de previsualizacion 5WH1+ y resaltar nodos y enlaces conectados. Desde 2026-10 el catalogo vivo es graph_ui sobre el store sldb (spec2viz catalog sync); este bundle es el export estatico.
