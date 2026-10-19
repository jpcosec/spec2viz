---
id: atom-catalogo-notacion-por-vista-y-metadatos-que-sobreviven-a-diagram-sync
title: 'Catalogo: notacion por vista y metadatos que sobreviven a diagram sync'
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:catalog
provenance: README.md
---

# Catalogo: notacion por vista y metadatos que sobreviven a diagram sync

## Answer

Una vista de vistas.yml puede fijar notation (ruta relativa al vistas.yml, nombre builtin o NotationDoc del store); catalog sync la usa y catalog validate la comprueba con UnknownNotationError y NotationMismatchError, sin escribir nada si una vista falla. diagram sync conserva category, nav y summary del SpecDoc cuando no recibe metadatos de catalogo.
