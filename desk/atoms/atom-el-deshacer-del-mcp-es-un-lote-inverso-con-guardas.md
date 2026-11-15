---
sldb:
  by: agent
  at: '2026-11-15T15:39:28Z'
  authority: generated
  via: save_document_payload
id: atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
title: El deshacer del MCP es un lote inverso con guardas
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: docs/decisiones/contrato-de-escritura-mcp.md
---

# El deshacer del MCP es un lote inverso con guardas

## Answer

La superficie MCP de specIR deshace escrituras de nivel 1 y 2 reaplicando, por sldb.api.apply_batch, el lote inverso que sldb devuelve al aplicar cada lote (create se borra, update vuelve al estado previo, delete se recrea), con guardas expected_source_hash del estado que dejó la aplicación: si alguien escribió después, sldb lo rechaza con ConflictError y no se escribe nada. specIR solo guarda esos inversos en la sesión del servidor y los reaplica en orden inverso; no construye inversos ni calcula guardas. Cubre los últimos lotes de la sesión; el nivel 3 no se deshace; la historia durable es git. Enmienda del 2026-11-15 (JP): construir el lote inverso es de sldb, no de specIR; antes decía que lo guardaba y armaba el servidor.
