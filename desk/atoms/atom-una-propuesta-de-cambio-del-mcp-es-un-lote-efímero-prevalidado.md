---
sldb:
  by: agent
  at: '2026-11-15T05:02:49Z'
  authority: generated
  via: create_document
id: atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado
title: Una propuesta de cambio del MCP es un lote efímero prevalidado
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: docs/decisiones/contrato-de-escritura-mcp.md
---

# Una propuesta de cambio del MCP es un lote efímero prevalidado

## Answer

En la superficie MCP de specIR una propuesta de cambio es un lote efímero en la forma de cambios de sldb.api.apply_batch (id, action, model, payload, path y los guardas que rellena el servidor), acompañado del resultado de su prevalidación. Proponer y validar no escriben en el store ni guardan estado en el servidor; aplicar recibe el mismo lote y lo aplica todo o nada con apply_batch. La validación sin escritura usa un dry_run público de SLDB, pedido a SLDB; specIR no importa módulos internos no declarados públicos.
