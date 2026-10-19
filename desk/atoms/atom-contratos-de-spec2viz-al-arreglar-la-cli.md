---
id: atom-contratos-de-spec2viz-al-arreglar-la-cli
title: Contratos de spec2viz al arreglar la CLI
five_wh_one_plus: how_not
tags:
- system:spec2viz
- topic:testing
provenance: desk/contexts/pill-pattern-preserve-spec2viz-contracts-while-fixing-cli-behavior.md
---

# Contratos de spec2viz al arreglar la CLI

## Answer

Al arreglar un fallo de la CLI (render, validate, schema, descubrimiento de renderers, alias legados) no se cambian los nombres canonicos de tipos de diagrama, los alias, las expectativas de los fixtures ni los artefactos generados para que el comando pase. Un crash no se arregla aflojando la validacion del esquema ni cambiando en silencio la salida canonica; si un golden cambia, se regenera a proposito y se explica el diff. No se agregan shims de compatibilidad fuera de la superficie legada nombrada (render, validate, lint, schema, build).
