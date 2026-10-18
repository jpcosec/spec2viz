---
id: atom-deskops-bridge-how
title: Deskops Integration Bridge Architecture
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:deskops
- topic:architecture
- topic:integration
provenance: spec2viz/deskops.py
---

# Deskops Integration Bridge Architecture

## Answer

El puente entre spec2viz y deskops vive en spec2viz/deskops.py y opera en cuatro pasos. Primero, parse_atoms escanea desk/atoms/*.md, separa el frontmatter YAML del cuerpo Markdown, toma el title normalizado a minusculas y la dimension five_wh_one_plus (what, why, how, how_not, when, where, for_whom) y lo indexa en window.ATOMS_DB[titulo][atoms][pregunta] con id y body. Segundo, render_deskops carga el registro vistas.yml, agrupa las vistas por category, lee la fuente de cada una (.mmd, .svg o .html) desde base_dir y construye la navegacion () y las secciones (). Tercero, en tiempo de compilacion reemplaza esos marcadores en la plantilla e inyecta window.ATOMS_DB como JSON en el script final del HTML. Cuarto, en el navegador, al hacer clic en un nodo de un diagrama Mermaid o SVG se normaliza su titulo, se busca en window.ATOMS_DB y se despliega el panel (Atom Drawer) con las pestañas 5WH1+ de ese componente. Desde 2026-10 el bundle es el export estatico; la superficie viva es graph_ui sobre el store sldb.
