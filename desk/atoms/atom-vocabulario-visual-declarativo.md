---
id: atom-vocabulario-visual-declarativo
title: Vocabulario visual declarativo
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:notation
provenance: docs/notation-contract.md
---

# Vocabulario visual declarativo

## Answer

La notacion de un tipo de diagrama es un conjunto de documentos del store sldb: un NotationDoc (nivel, tipo de diagrama, layout, marcas, glifos y links), un GlyphDoc por clase de elemento (modelo mas predicado where, en la gramatica de sldb find --where, hacia forma, rotulo, keyword y compartimentos) y un LinkDoc por relacion (relation hacia draw line|nest|lane|cell|axis, trazo, terminales y rotulos de extremo; '*' es el comodin). spec2viz trae una por tipo en spec2viz/notations/ y las escribe con spec2viz notation sync.
