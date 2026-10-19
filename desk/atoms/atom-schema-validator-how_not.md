---
id: atom-schema-validator-how_not
title: Schema Validator
five_wh_one_plus: how_not
tags:
- system:spec2viz
- topic:validator
provenance: spec2viz/validator.py
---

# Schema Validator

## Answer

No debe mutar el modelo ni dejar pasar referencias rotas en silencio. Una referencia huerfana o un ciclo de herencia lanza spec2viz.exceptions.ValidationError (no ParseError, que es del loader), y la CLI lo muestra y sale con error.
