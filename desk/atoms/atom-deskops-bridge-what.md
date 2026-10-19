---
id: atom-deskops-bridge-what
title: Deskops Integration Bridge
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:deskops
provenance: spec2viz/deskops.py
---

# Deskops Integration Bridge

## Answer

El Deskops Integration Bridge (spec2viz/deskops.py) es la capa que construye el bundle HTML estatico del catalogo a partir de vistas.yml, los atomos de desk/atoms y las referencias y aristas del store sldb (SldbAtomResolver). Desde 2026-10 el catalogo vivo es graph_ui leyendo el store (catalog sync); el bundle es el export.
