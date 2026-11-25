---
sldb:
  by: agent
  at: '2026-11-25T03:37:32Z'
  authority: generated
  via: create_document
id: atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir
title: specir mcp levanta el server MCP de sldb con la extension de specIR
five_wh_one_plus: how
tags:
- system:ir
- topic:specir-mcp
---

# specir mcp levanta el server MCP de sldb con la extension de specIR

## Answer

specir mcp --store <store> [--level N] [--actor A] llama sldb.mcp.server.serve con extensions=('specir.mcp_extension:register',): specIR tiene su propio punto de entrada MCP sin duplicar el server, la guarda ni el undo de sldb.
