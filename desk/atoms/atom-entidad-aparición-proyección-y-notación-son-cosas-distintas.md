---
sldb:
  by: agent
  at: '2026-11-12T00:48:14Z'
  authority: generated
  via: save_document_payload
id: atom-entidad-aparición-proyección-y-notación-son-cosas-distintas
title: Identidad semántica, aparición, proyección, notación y formato de autoría son
  cosas distintas
five_wh_one_plus: what
tags:
- system:specir
- topic:identidad
- topic:proyecciones
- layer:modelo
provenance: fundamentos_modelado_semantico_mcp.md
---

# Identidad semántica, aparición, proyección, notación y formato de autoría son cosas distintas

## Answer

La fuente semántica de specIR es el grafo tipado de SLDB. Se distinguen cinco cosas: (1) entidad semántica, lo que existe en el dominio o sistema (Post, PublishPost, POST /posts/{id}/publish), con una sola identidad en el grafo; (2) aparición, la presencia de esa entidad en una vista o diagrama; (3) proyección, el criterio que selecciona y organiza elementos y relaciones del grafo para una finalidad; (4) notación, las reglas para dibujarlos, que no redefinen su identidad ni su significado; (5) formato de autoría, el archivo en que alguien escribe o intercambia un diagrama. El YAML de spec de spec2viz es un formato de autoría e intercambio, válido al menos mientras dure la paridad con spec2viz: lo que declara entra al grafo y no constituye una segunda identidad. Dos diagramas pueden mostrar el mismo objeto sin duplicarlo. Si el YAML se conserva como formato permanente es una decisión pendiente, incluida en la candidata de cobertura de spec2viz.
