---
id: atom-viewdoc-vista-portable-de-la-gramatica-de-proyeccion
title: 'ViewDoc: vista portable de la gramatica de proyeccion'
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:notation
provenance: docs/notation-contract.md
---

# ViewDoc: vista portable de la gramatica de proyeccion

## Answer

ViewDoc (spec2viz.sldb_models) es una vista guardada en el store: que documentos entran (union de entradas model + where), que tipos de relacion se conservan, en que direccion (both, outgoing, incoming), y con que notacion y override de layout se dibuja (style layered o rings, ring_field). Es portable porque solo nombra modelos, relaciones y una notacion, nunca ids de nodo ni rutas de store. spec2viz define y valida el modelo; graph_ui la evalua con sldb.api.graph y la crea y guarda por sldb.
