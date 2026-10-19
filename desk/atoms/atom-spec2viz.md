---
id: atom-spec2viz
title: spec2viz
five_wh_one_plus: what
tags: []
provenance: README.md
---

# spec2viz

## Answer

spec2viz compila specs YAML semanticas de diagramas (secuencia, estado, componentes, actividad, despliegue, clases, matriz, reflection) en una IR agnostica y las proyecta a Mermaid, PlantUML, D2, Vega y HTML. Ademas materializa cada spec como namespace del store sldb (SpecDoc, SpecNodeDoc, RelationDoc) y declara el vocabulario visual (NotationDoc, GlyphDoc, LinkDoc) con el que graph_ui dibuja los specs en vivo; notation view es el unico interprete de ese contrato. El YAML es la verdad, versionable y editable por LLM; todo lo demas es proyeccion.
