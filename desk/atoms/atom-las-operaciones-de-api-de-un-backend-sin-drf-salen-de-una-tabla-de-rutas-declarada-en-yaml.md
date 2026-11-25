---
sldb:
  by: agent
  at: '2026-11-25T06:37:42Z'
  authority: generated
  via: create_document
id: atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml
title: Las operaciones de API de un backend sin DRF salen de una tabla de rutas declarada
  en YAML
five_wh_one_plus: how
tags:
- system:ir
- topic:routes-declaradas
---

# Las operaciones de API de un backend sin DRF salen de una tabla de rutas declarada en YAML

## Answer

specir.extract.extract_routes lee un YAML de rutas (method, route, title) y escribe ApiOperationDoc con origen declarado, idempotentes; rechaza el choque con una derivada y reporta en stale_declared las que salieron de la tabla.
