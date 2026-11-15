---
sldb:
  by: agent
  at: '2026-11-15T05:02:55Z'
  authority: generated
  via: create_document
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

La superficie MCP de specIR deshace escrituras de nivel 1 y 2 aplicando, por sldb.api.apply_batch, el lote inverso que el servidor guardó al aplicar (update vuelve al payload anterior, create se borra, delete se recrea con su payload y ruta, move vuelve), con guardas expected_source_hash del estado que dejó la aplicación: si alguien escribió después, el deshacer falla con ConflictError. Cubre los últimos lotes de la sesión del servidor; el nivel 3 no se deshace. La historia durable es git; si SLDB entrega un deshacer nativo, specIR lo adopta y retira el suyo.
