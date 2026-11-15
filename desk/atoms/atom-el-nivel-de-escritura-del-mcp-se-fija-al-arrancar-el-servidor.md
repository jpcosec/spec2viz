---
sldb:
  by: agent
  at: '2026-11-15T05:02:53Z'
  authority: generated
  via: create_document
id: atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor
title: El nivel de escritura del MCP se fija al arrancar el servidor
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: docs/decisiones/contrato-de-escritura-mcp.md
---

# El nivel de escritura del MCP se fija al arrancar el servidor

## Answer

El nivel de escritura permitido de la superficie MCP de specIR (0 lectura, 1 contenido, 2 reglas y tipos de relación, 3 modelos; acumulativos) se declara al arrancar el servidor, por cada store montado. Sin declaración el nivel es 0, solo lectura. El nivel nunca sale de un argumento de un tool, de un documento que el agente pueda escribir ni del actor declarado; un tool de nivel superior al permitido responde error sin escribir.
