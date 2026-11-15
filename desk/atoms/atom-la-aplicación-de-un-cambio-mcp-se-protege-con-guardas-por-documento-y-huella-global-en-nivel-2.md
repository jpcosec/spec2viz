---
sldb:
  by: agent
  at: '2026-11-15T05:02:51Z'
  authority: generated
  via: create_document
id: atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2
title: La aplicación de un cambio MCP se protege con guardas por documento y huella
  global en nivel 2
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: docs/decisiones/contrato-de-escritura-mcp.md
---

# La aplicación de un cambio MCP se protege con guardas por documento y huella global en nivel 2

## Answer

Al validar, el servidor MCP de specIR anota expected_source_hash de cada documento que el lote toca (update, move, delete, untrack) y create o track exigen que el documento no exista; apply_batch rechaza con ConflictError un guarda que no coincide. Los guardas los rellena el servidor, nunca el agente. Para escrituras de nivel 2 (reglas), cuya validez depende de todas las aristas del tipo, se exige además store_hash como precondición atómica cuando SLDB la entregue; hasta entonces el nivel 2 vuelve a simular su efecto justo antes de apply_batch y acepta la carrera residual.
