---
id: atom-pydantic-models-how
title: Pydantic Schema Models
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:models
provenance: spec2viz/models/
---

# Pydantic Schema Models

## Answer

Definen subclases de BaseDiagram (un modelo por tipo de diagrama, discriminado por 'type') y submodelos BaseModel de Pydantic v2 con campos requeridos y Field con descripcion. La estrictez es deliberada por nivel. BaseDiagram, Metadata, Style y los submodelos de activity, component, deployment, state, matrix y reflection usan extra='ignore' para tolerar claves nuevas o de otras herramientas en el YAML; los de class, sequence y catalog usan extra='forbid'. Los campos refs y atoms de cada elemento enlazan documentos y atomos del store sldb.
