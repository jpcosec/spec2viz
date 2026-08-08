---
id: atom-pydantic-models-how_not
title: Pydantic Schema Models
five_wh_one_plus: how_not
tags:
- system:spec2viz
- topic:models
provenance: spec2viz/models/
---

# Pydantic Schema Models - HOW_NOT

## Answer

No deben permitir campos adicionales arbitrarios sin tipar ni relajar la validación usando `extra="ignore"` en modelos de producción.
