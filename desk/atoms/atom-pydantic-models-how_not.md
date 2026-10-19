---
id: atom-pydantic-models-how_not
title: Pydantic Schema Models
five_wh_one_plus: how_not
tags:
- system:spec2viz
- topic:models
provenance: spec2viz/models/
---

# Pydantic Schema Models

## Answer

No deben declarar campos sin tipo ni aflojar los requeridos para que un spec roto cargue. Cambiar extra='ignore' por 'forbid' en los modelos de spec rompe YAML existentes y no se hace sin decision; cambiar 'forbid' por 'ignore' en clases, secuencia o catalogo oculta errores de autor. La validacion semantica (referencias huerfanas) no va aqui sino en spec2viz.validator.
