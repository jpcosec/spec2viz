---
sldb:
  by: agent
  at: '2026-11-15T05:05:34Z'
  authority: generated
  via: create_document
id: atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla
title: La procedencia en specIR tiene dos ejes y la autoridad de SLDB se asigna por
  tabla
five_wh_one_plus: what
tags:
- system:specir
- topic:procedencia
- layer:modelo
provenance: docs/decisiones/procedencia-y-divergencia.md
---

# La procedencia en specIR tiene dos ejes y la autoridad de SLDB se asigna por tabla

## Answer

Cada nodo y relación de specIR declara dos ejes en sus campos de dominio (en una relación, en RelationDoc.attributes): origen, uno de observado (lo leyó un extractor tal cual), derivado (regla estática enunciada sobre lo observado), inferido (propuesto por un LLM) o declarado (escrito con intención, no extraído); y verificacion, uno de sin_verificar, verificado o refutado, con verificado_por y evidencia. La authority del bloque sldb se asigna por esta tabla y no se reinventa: observado = generated con from code:<ruta>::<símbolo>; derivado = theorem con from de las fuentes de la regla; inferido = authored con by agent:<id>; declarado = authored. Equivalencias: la lista observado/inferido/validado de fundamentos §7 es origen observado o inferido más verificacion verificado; la lista observado/derivado estáticamente/inferencia de LLM/verificado de Plan_IR fase 5 son los tres primeros orígenes más verificacion verificado.
