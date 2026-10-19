---
id: atom-cli-entrypoint-what
title: CLI Entrypoint
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:cli
provenance: spec2viz/cli.py
---

# CLI Entrypoint

## Answer

spec2viz.cli es la interfaz de linea de comandos construida con Click, con los grupos diagram, notation y catalog. Renderiza y valida specs, las sincroniza al store sldb como namespace, declara y sincroniza la notacion con la que graph_ui dibuja, y construye o sincroniza el catalogo (vistas.yml); el bundle HTML es el export estatico.
