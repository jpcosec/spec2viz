---
id: atom-pydantic-models-how
title: Pydantic Schema Models
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:models
provenance: spec2viz/models/
---

# Pydantic Schema Models - HOW

## Answer

Definen subclases de `BaseDiagram` y `BaseModel` configuradas con `ConfigDict(extra="forbid")` para rechazar campos no reconocidos y validar campos requeridos.
